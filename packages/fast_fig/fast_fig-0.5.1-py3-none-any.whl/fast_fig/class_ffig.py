"""fast_fig simplifies figure handling with matplotlib:
- predefinied templates
- figure instantiation in a class object
- simplified handling (e.g. plot with vectors)

import fast_fig
# very simple example
fig = fast_fig.FFig()
fig.plot()
fig.show()

# more complex example
fig = fast_fig.FFig("l", nrows=2, sharex=True)  # create figure with template l=large
fig.plot([1, 2, 3, 1, 2, 3, 4, 1, 1])  # plot first data set
fig.title("First data set")  # set title for subplot
fig.subplot()  # set focus to next subplot/axis
fig.plot([0, 1, 2, 3, 4], [0, 1, 1, 2, 3], label="random")  # plot second data set
fig.legend()  # generate legend
fig.grid()  # show translucent grid to highlight major ticks
fig.xlabel("Data")  # create xlabel for second axis
fig.save("fig1.png", "pdf")  # save figure to png and pdf

# The following handlers can be used to access all matplotlib functionality:
# - fig.handler_fig
# - fig.handler_plot
# - fig.handler_axis
# - fig.current_axis

"""

# %%
__author__ = "Fabian Stutzki"
__email__ = "fast@fast-apps.de"
__version__ = "0.2.6"

import pathlib
import os
import numpy as np
from packaging import version
import matplotlib
import matplotlib.pyplot
from cycler import cycler
from fast_fig.presets import define_presets


# %%
class FFig:
    """
    Figure simplifies handling of matplotlib

    Use as
    from fast_fig import FFig
    fig = FFig('m')
    fig.plot([0,1,2,3,4],[0,1,1,2,3])
    fig.save('test.png')

    @author: fstutzki

    """

    def __init__(self, *args, template="m", nrows=1, ncols=1, **kwargs):
        """Set default values and create figure: fig = FFig("OL", nrows=2, ncols=2)"""

        # Assign unnamed arguments
        if len(args) == 1:
            if isinstance(args[0], int):
                nrows = args[0]
            else:
                template = args[0]
        elif len(args) == 2:
            if isinstance(args[0], int):
                nrows = args[0]
                ncols = args[1]
            else:
                template = args[0]
                nrows = args[1]
        elif len(args) == 3:
            template = args[0]
            nrows = args[1]
            ncols = args[2]
        elif len(args) > 3:
            raise ValueError("Too many arguments! FFig() accepts a maximum of 3 unnamed arguments.")

        kwargs.setdefault("isubplot", 0)
        kwargs.setdefault("sharex", False)
        kwargs.setdefault("sharey", False)
        kwargs.setdefault("show", True)
        kwargs.setdefault("vspace", None)
        kwargs.setdefault("hspace", None)
        kwargs.setdefault("presets", None)

        # Initialize dictionary with presets
        self.presets = define_presets(kwargs["presets"])

        # check if template exists (ignoring case), otherwise set template m (default)
        template = template.lower()
        if template not in self.presets:
            template = "m"

        # Fill undefined kwargs with presets
        for key in ["width", "height", "fontfamily", "fontsize", "linewidth"]:
            kwargs.setdefault(key, self.presets[template][key])

        # apply parameters to matplotlib
        matplotlib.rc("font", size=kwargs["fontsize"])
        matplotlib.rc("font", family=kwargs["fontfamily"])
        matplotlib.rc("lines", linewidth=kwargs["linewidth"])

        # convert colors to ndarray and scale to 1 instead of 255
        self.colors = {}
        for iname, icolor in self.presets["colors"].items():
            if np.max(icolor) > 1:
                self.colors[iname] = np.array(icolor) / 255

        # define cycle with colors, color_seq and linestyle_seq
        self.set_cycle(self.colors, self.presets["color_seq"], self.presets["linestyle_seq"])

        # store global variables
        self.figshow = kwargs["show"]  # show figure after saving
        self.axe_current = 0
        self.handle_bar = None
        self.handle_plot = None
        self.handle_surface = None
        self.linewidth = kwargs["linewidth"]

        # Create figure
        self.handle_fig = matplotlib.pyplot.figure()
        self.handle_fig.set_size_inches(kwargs["width"] / 2.54, kwargs["height"] / 2.54)
        self.subplot(
            nrows=nrows,
            ncols=ncols,
            index=kwargs["isubplot"],
            sharex=kwargs["sharex"],
            sharey=kwargs["sharey"],
            vspace=kwargs["vspace"],
            hspace=kwargs["hspace"],
        )

    #        if template.lower() == 'square':
    #            self.axeC.margins(0)
    #            self.axeC.axis('off')
    #            self.axeC.set_position([0, 0, 1, 1])

    def subplot(
        self,
        *args,
        nrows=None,
        ncols=None,
        index=None,
        sharex=False,
        sharey=False,
        vspace=None,
        hspace=None,
    ):
        """
        Set current axis/subplot: fig.subplot(0) for first subplot
        or fig.subplot() for next subplot
        """

        num_args = len(args)
        if num_args == 0:
            # increase current axe handle by 1
            self.axe_current += 1
        elif num_args == 1:
            # define current axe handle
            self.axe_current = args[0]
        elif num_args in (2, 3):
            # generate new subplot
            nrows = args[0]
            ncols = args[1]
        else:
            raise ValueError("subplot() takes 0 to 3 unnamed arguments")

        if nrows is not None or ncols is not None:
            # generate new subplot
            if nrows is None:
                nrows = 1
            if ncols is None:
                ncols = 1
            self.subplot_nrows = nrows
            self.subplot_ncols = ncols
            self.subplot_sharex = sharex
            self.subplot_sharey = sharey
            self.subplot_vspace = vspace
            self.subplot_hspace = hspace
            if num_args == 3:
                self.axe_current = args[2]
            else:
                self.axe_current = 0
            try:
                self.handle_fig.clf()
                self.handle_fig, self.handle_axis = matplotlib.pyplot.subplots(
                    nrows=self.subplot_nrows,
                    ncols=self.subplot_ncols,
                    num=self.handle_fig.number,
                    sharex=self.subplot_sharex,
                    sharey=self.subplot_sharey,
                )
            except Exception as excpt:
                print("subplot(): Matplotlib cannot generate subplots.")
                print(excpt)

        # overwrite axe_current with named argument
        if index is not None:
            self.axe_current = index

        # set current axe handle
        self.axe_current = self.axe_current % (self.subplot_nrows * self.subplot_ncols)
        if self.subplot_nrows == 1 and self.subplot_ncols == 1:
            self.current_axis = self.handle_axis
        elif self.subplot_nrows > 1 and self.subplot_ncols > 1:
            isuby = self.axe_current // self.subplot_ncols
            isubx = self.axe_current % self.subplot_ncols
            self.current_axis = self.handle_axis[isuby][isubx]
        else:
            self.current_axis = self.handle_axis[self.axe_current]

    #        if np.size(self.figH.get_axes()) <= self.axe_current:
    # self.axeC = matplotlib.pyplot.subplot(
    #     self.subplot_nrows, self.subplot_ncols, self.axe_current
    # )  # ,True,False)

    #        else:
    #        print(self.figH.get_axes())
    #        self.axeC = self.figH.get_axes()[self.axe_current-1]
    #        return self.axeC

    def suptitle(self, *args, **kwargs):
        """Set super title for the whole figure"""
        self.handle_fig.suptitle(*args, **kwargs)

    def bar_plot(self, *args, **kwargs):
        """Generate bar plot"""
        self.handle_bar = self.current_axis.bar(*args, **kwargs)
        return self.handle_bar

    def plot(
        self,
        mat=np.array([[1, 2, 3, 4, 5, 6, 7], np.random.randn(7), 2 * np.random.randn(7)]),
        *args,
        **kwargs,
    ):
        """plot() generates a line plot"""
        if np.ndim(mat) > 1:
            if np.shape(mat)[0] > np.shape(mat)[1]:
                mat = mat.T
            for imat in mat[1:]:
                self.handle_plot = self.current_axis.plot(mat[0, :], imat, *args, **kwargs)
        else:
            self.handle_plot = self.current_axis.plot(mat, *args, **kwargs)
        return self.handle_plot

    # def plot(
    #     self,
    #     *args,
    #     **kwargs,
    # ):
    #     """Generate line plot"""
    #     if args:
    #         # if np.ndim(args[0]) > 1:
    #         #     if np.shape(args[0])[0] > np.shape(args[0])[1]:
    #         #         args[0] = args[0].T
    #         #     for irow in args[0][1:]:
    #         #         print("Plot")
    #         #         print(args[0][0,:])
    #         #         print(irow)
    #         #         self.plotH = self.axeC.plot(args[0][0, :], irow, **kwargs)
    #         #     return self.plotH
    #         # else:
    #         print(args)
    #         self.plotH = self.axeC.plot(*args, **kwargs)
    #         return self.plotH
    #     else:
    #         self.plot(np.array(
    #             [[1, 2, 3, 4, 5, 6, 7, 8], np.random.randn(8), 2 * np.random.randn(8)]
    #         ),**kwargs)

    def semilogx(self, *args, **kwargs):
        """Semi-log plot on x axis"""
        self.plot(*args, **kwargs)
        self.xscale("log")

    def semilogy(self, *args, **kwargs):
        """Semi-log plot on y axis"""
        self.plot(*args, **kwargs)
        self.yscale("log")

    def fill_between(self, *args, color=None, alpha=0.1, linewidth=0, **kwargs):
        """Fill area below / between lines"""
        if color is None:
            color = self.last_color()
        self.current_axis.fill_between(
            *args, color=color, alpha=alpha, linewidth=linewidth, **kwargs
        )

    def last_color(self):
        """Returns the last color code used by plot"""
        return self.handle_plot[0].get_color()

    def pcolor(self, *args, **kwargs):
        """2D area plot"""
        if "cmap" not in kwargs:
            kwargs["cmap"] = "nipy_spectral"
        self.handle_surface = self.current_axis.pcolormesh(*args, **kwargs)
        return self.handle_surface

    def pcolor_log(self, *args, vmin=False, vmax=False, **kwargs):
        """2D area plot with logarithmic scale"""
        if "cmap" not in kwargs:
            kwargs["cmap"] = "nipy_spectral"
        kwargs_log = {}
        if vmin is not False:
            kwargs_log["vmin"] = vmin
        if vmax is not False:
            kwargs_log["vmax"] = vmax
        kwargs["norm"] = matplotlib.colors.LogNorm(**kwargs_log)
        self.handle_surface = self.current_axis.pcolormesh(*args, **kwargs)
        return self.handle_surface

    def pcolor_square(self, *args, **kwargs):
        """2D area plot with axis equal and off"""
        if "cmap" not in kwargs:
            kwargs["cmap"] = "nipy_spectral"
        self.handle_surface = self.current_axis.pcolormesh(*args, **kwargs)
        self.current_axis.axis("off")
        self.current_axis.set_aspect("equal")
        self.current_axis.set_xticks([])
        self.current_axis.set_yticks([])
        return self.handle_surface

    def contour(self, *args, **kwargs):
        """2D contour plot"""
        self.handle_surface = self.current_axis.contour(*args, **kwargs)
        return self.handle_surface

    def scatter(self, *args, **kwargs):
        """Plot scattered data"""
        self.handle_surface = self.current_axis.scatter(*args, **kwargs)
        return self.handle_surface

    def colorbar(self, *args, **kwargs):
        """Add colorbar to figure"""
        self.handle_fig.colorbar(*args, self.handle_surface, ax=self.current_axis, **kwargs)

    #        self.axeC.colorbar(*args,**kwargs)
    def axis(self, *args, **kwargs):
        """Access axis properties such as 'off'"""
        self.current_axis.axis(*args, **kwargs)

    def axis_aspect(self, *args, **kwargs):
        """Access axis aspect ration"""
        self.current_axis.set_aspect(*args, **kwargs)

    def grid(self, *args, color="grey", alpha=0.2, **kwargs):
        """Access axis aspect ration"""
        self.current_axis.grid(*args, color=color, alpha=alpha, **kwargs)

    def annotate(self, *args, **kwargs):
        """Annotation to figure"""
        self.current_axis.annotate(*args, **kwargs)

    def text(self, *args, **kwargs):
        """Text to figure"""
        self.current_axis.text(*args, **kwargs)

    def title(self, *args, **kwargs):
        """Set title for current axis"""
        self.current_axis.set_title(*args, **kwargs)

    def xscale(self, *args, **kwargs):
        """Set x-axis scaling"""
        self.current_axis.set_xscale(*args, **kwargs)

    def yscale(self, *args, **kwargs):
        """Set y-axis scaling"""
        self.current_axis.set_yscale(*args, **kwargs)

    def xlabel(self, *args, **kwargs):
        """Set xlabel for current axis"""
        self.current_axis.set_xlabel(*args, **kwargs)

    def ylabel(self, *args, **kwargs):
        """Set ylabel for current axis"""
        self.current_axis.set_ylabel(*args, **kwargs)

    def xlim(self, xmin=np.inf, xmax=-np.inf):
        """Set limits for current x-axis: xlim(0,1) or xlim()"""
        try:
            if np.size(xmin) == 2:
                xmax = xmin[1]
                xmin = xmin[0]
            elif xmin == np.inf and xmax == -np.inf:
                for iline in self.current_axis.lines:
                    xdata = iline.get_xdata()
                    xmin = np.minimum(xmin, np.nanmin(xdata))
                    xmax = np.maximum(xmax, np.nanmax(xdata))
            if version.parse(matplotlib.__version__) >= version.parse("3"):
                if np.isfinite(xmin):
                    self.current_axis.set_xlim(left=xmin)
                if np.isfinite(xmax):
                    self.current_axis.set_xlim(right=xmax)
            else:
                if np.isfinite(xmin):
                    self.current_axis.set_xlim(xmin=xmin)
                if np.isfinite(xmax):
                    self.current_axis.set_xlim(xmax=xmax)
        except Exception as excpt:
            print("xlim() throws exception:")
            print(excpt)
            # pass

    def ylim(self, ymin=np.inf, ymax=-np.inf):
        """Set limits for current y-axis: ylim(0,1) or ylim()"""
        try:
            if np.size(ymin) == 2:
                ymax = ymin[1]
                ymin = ymin[0]
            elif ymin == np.inf and ymax == -np.inf:
                for iline in self.current_axis.lines:
                    ydata = iline.get_ydata()
                    ymin = np.minimum(ymin, np.nanmin(ydata))
                    ymax = np.maximum(ymax, np.nanmax(ydata))
            if version.parse(matplotlib.__version__) >= version.parse("3"):
                if np.isfinite(ymin):
                    self.current_axis.set_ylim(bottom=ymin)
                if np.isfinite(ymax):
                    self.current_axis.set_ylim(top=ymax)
            else:
                if np.isfinite(ymin):
                    self.current_axis.set_ylim(ymin=ymin)
                if np.isfinite(ymax):
                    self.current_axis.set_ylim(ymax=ymax)
        except Exception as excpt:
            print("ylim() throws exception:")
            print(excpt)
            # pass

    def legend(self, *args, labels=None, **kwargs):
        """Insert legend based on labels given in plot(x,y,label='Test1') etc."""
        if labels is not None:
            ilabel = 0
            for iline in self.current_axis.lines:
                iline.set_label(labels[ilabel])
                ilabel += 1
        _, labels = self.current_axis.get_legend_handles_labels()
        if np.size(self.current_axis.lines) != 0 and len(labels) != 0:
            self.current_axis.legend(*args, **kwargs)

    def legend_entries(self):
        """Returns handle and labels of legend"""
        handles, labels = self.current_axis.get_legend_handles_labels()
        return handles, labels

    def legend_count(self):
        """Return number of legend entries"""
        handles, _ = self.current_axis.get_legend_handles_labels()
        return np.size(handles)

    def set_cycle(self, colors, color_seq, linestyle_seq):  # ,linewidth=False):
        """Call to set color and linestyle cycle (will be used in this order)"""

        # generate cycle from color_seq and linestyle_seq
        color_list = [colors[icolor] for icolor in color_seq if icolor in colors]
        cyc_color = np.tile(color_list, (np.size(linestyle_seq), 1))
        cyc_linestyle = np.repeat(linestyle_seq, np.shape(color_list)[0])
        try:
            matplotlib.rc(
                "axes",
                prop_cycle=(cycler("color", cyc_color) + cycler("linestyle", cyc_linestyle)),
            )
            if hasattr(self, "axeC"):
                self.current_axis.set_prop_cycle(
                    cycler("color", cyc_color) + cycler("linestyle", cyc_linestyle)
                )
        except Exception as excpt:
            print("set_cycle(): Cannot set cycle for color and linestyle")
            print(excpt)

    def set_parameters(self):
        """Set useful figure parameters, called automatically by save
        and show function
        """
        # try:
        #     if (
        #         self.axeC.get_xscale() != "log"
        #     ):  # Otherwise xticks get missing on saving/showing- seems to be a bug
        #         self.axeH.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(7))
        # except:
        #     pass
        try:
            self.handle_fig.tight_layout()
        except Exception as excpt:
            print("set_parameters(): Tight layout cannot be set!")
            print(excpt)

        if self.subplot_hspace is not None and self.subplot_nrows > 1:
            self.handle_fig.subplots_adjust(hspace=self.subplot_hspace)
        if self.subplot_vspace is not None and self.subplot_ncols > 1:
            self.handle_fig.subplots_adjust(vspace=self.subplot_vspace)

    def watermark(self, img, *args, xpos=100, ypos=100, alpha=0.15, zorder=1, **kwargs):
        """Include watermark image to plot"""
        if os.path.isfile(img):
            self.handle_fig.figimage(img, xpos, ypos, alpha=alpha, zorder=zorder, *args, **kwargs)
        else:
            print("watermark(): File not found")

    def show(self):
        """Show figure in interactive console (similar to save)"""
        self.set_parameters()
        matplotlib.pyplot.show()  # block=False)

    def save(self, filename, *args, **kwargs):
        """Save figure to png, pdf: save('test.png',600,'pdf')"""
        dpi = 300
        fileparts = filename.split(".")
        fileformat = set()
        fileformat.add(fileparts[-1])
        filename = filename.replace("." + fileparts[-1], "")
        for attribute in args:
            if isinstance(attribute, int):
                dpi = attribute
            else:
                fileformat.add(attribute)
        if "dpi" not in kwargs:
            kwargs["dpi"] = dpi

        self.set_parameters()
        for iformat in fileformat:
            try:
                pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
                self.handle_fig.savefig(filename + "." + iformat, **kwargs)
            except Exception as excpt:
                print(f"save(): Figure cannot be saved to {filename}.{iformat}")
                print(excpt)
        if self.figshow:
            matplotlib.pyplot.show()  # block=False)
        else:
            matplotlib.pyplot.draw()

    def clear(self, *args, **kwargs):
        """Clear figure content in order to reuse figure"""
        self.handle_fig.clf(*args, **kwargs)

    def close(self):
        """Close figure"""
        #        self.figH.close(*args,**kwargs)
        try:
            matplotlib.pyplot.close(self.handle_fig)
        except Exception as excpt:
            print("close(): Figure cannot be closed")
            print(excpt)


# %%
if __name__ == "__main__":
    fig = FFig()
    fig.plot()
    fig.show()
