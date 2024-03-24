"""
``holoviews`` visualizations in ``hiveplotlib``.

Currently, ``hiveplotlib`` supports a ``bokeh`` and ``matplotlib`` backend for ``holoviews``.
"""

# __all__ = []

try:
    import holoviews as hv
except ImportError:  # pragma: no cover
    raise ImportError(
        "`holoviews` not installed, but can be installed by running `pip install hiveplotlib[holoviews]`"
    )

from typing import Hashable, List, Literal, Optional, Union, get_args

import numpy as np

from hiveplotlib import P2CP, HivePlot
from hiveplotlib.utils import polar2cartesian
from hiveplotlib.viz.base import edge_viz_preparation, get_axis_label_alignment
from hiveplotlib.viz.input_checks import input_check

SUPPORTED_BACK_ENDS = Literal["bokeh", "matplotlib"]


def _get_current_hv_backend() -> SUPPORTED_BACK_ENDS:
    """
    Get the current active ``holoviews`` backend.

    :return: string of current backend (i.e. ``bokeh`` or ``matplotlib``.)
    :raise: ``ValueError`` if anything other than one of the ``SUPPORTED_BACK_ENDS`` provided.
    """
    current_backend = hv.Store.current_backend
    assert current_backend in get_args(SUPPORTED_BACK_ENDS), (
        f"User using holoviews backend {current_backend} "
        f"but hiveplotlib currently only supports {get_args(SUPPORTED_BACK_ENDS)}"
    )
    return current_backend


def _holoviews_fig_modification(
    hive_plot: HivePlot,
    fig: hv.Overlay,
    buffer: float = 0.3,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    axes_off: bool = True,
    xaxis: Optional[Literal["bare", "bottom", "top"]] = "bottom",
    yaxis: Optional[Literal["bare", "left", "right"]] = "left",
    overlay_kwargs: Optional[dict] = None,
) -> hv.Overlay:
    """
    Modify ``holoviews.Overlay`` with some Hiveplotlib-friendly defaults.

    :param hive_plot: ``HivePlot`` instance to plot. Should never take a ``P2CP`` instance.
    :param fig: ``holoviews.Overlay`` to modify.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10.
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10.
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``hive_plot``.
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param xaxis: placement of x axis. Only used if ``axes_off=False``.
    :param yaxis: placement of y axis. Only used if ``axes_off=False``.
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :return: ``holoviews.Overlay``.
    """
    backend = _get_current_hv_backend()

    if overlay_kwargs is None:
        overlay_kwargs = {}

    # set default title to nothing
    overlay_kwargs.setdefault("title", "")

    # only difference in different backend defaults is how to specify figure size
    if backend == "matplotlib":
        if width is None:
            width = 10
        if height is None:
            height = 10
        overlay_kwargs.setdefault("fig_inches", (width, height))
    elif backend == "bokeh":
        if width is None:
            width = 600
        if height is None:
            height = 600
        overlay_kwargs.setdefault("width", width)
        overlay_kwargs.setdefault("height", height)
        overlay_kwargs.setdefault("data_aspect", 1)
        overlay_kwargs.setdefault("data_aspect", 1)

    # can only center the plot if you have axes
    if center_plot and hive_plot.max_polar_end is not None:
        # center plot at (0, 0)
        max_radius = hive_plot.max_polar_end
        # throw in a minor buffer
        buffer_radius = buffer * max_radius
        max_radius += buffer_radius

        fig_bounds = (-max_radius, max_radius)
        overlay_kwargs.setdefault("xlim", fig_bounds)
        overlay_kwargs.setdefault("ylim", fig_bounds)

    if axes_off:
        overlay_kwargs["xaxis"] = None
        overlay_kwargs["yaxis"] = None
        if backend == "bokeh":
            overlay_kwargs["backend_opts"] = {"plot.outline_line_color": None}
    else:
        overlay_kwargs["xaxis"] = xaxis
        overlay_kwargs["yaxis"] = yaxis
        if backend == "bokeh":
            overlay_kwargs["backend_opts"] = {"plot.outline_line_color": "#e5e5e5"}

    return fig.opts(**overlay_kwargs)


def axes_viz(
    instance: Union[HivePlot, P2CP],
    fig: Optional[hv.Overlay] = None,
    buffer: float = 0.3,
    show_axes_labels: bool = True,
    axes_labels_buffer: float = 1.1,
    axes_labels_fontsize: int = 16,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    axes_off: bool = True,
    overlay_kwargs: Optional[dict] = None,
    text_kwargs: Optional[dict] = None,
    **curve_kwargs,
) -> hv.Overlay:
    """
    ``holoviews`` visualization of axes in a ``HivePlot`` or ``P2CP`` instance.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw axes.
    :param fig: default ``None`` builds new overlay. If an overlay is specified, axes will be drawn on that overlay.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for axes labels.
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``instance``.
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :param text_kwargs: additional kwargs passed to
        `holoviews.Text() <https://holoviews.org/reference/elements/bokeh/Text.html>`__ call.
    :param curve_kwargs: additional params that will be applied to all hive plot axes. Note, these are kwargs that
        affect a `holoviews.Curve() <https://holoviews.org/reference/elements/bokeh/Curve.html>`__ call.
    :return: ``holoviews.Overlay``.
    """
    backend = _get_current_hv_backend()

    # some default kwargs for the axes
    curve_kwargs.setdefault("color", "black")
    if backend == "bokeh":
        curve_kwargs.setdefault("line_alpha", 0.5)
        curve_kwargs.setdefault("line_width", 1.5)
    elif backend == "matplotlib":
        curve_kwargs.setdefault("alpha", 0.5)
        curve_kwargs.setdefault("linewidth", 1.5)

    hive_plot, _, warning_raised = input_check(instance, objects_to_plot="axes")

    if warning_raised:
        return None

    if text_kwargs is None:
        text_kwargs = {}

    axis_plots = []
    for axis in hive_plot.axes.values():
        axis_range = np.row_stack([axis.start, axis.end])
        axis_plots.append(hv.Curve(axis_range, group="Axes").opts(**curve_kwargs))

    axis_fig = hv.Overlay(axis_plots)

    if show_axes_labels:
        axis_fig = label_axes(
            instance=hive_plot,
            fig=axis_fig,
            center_plot=False,
            axes_labels_buffer=axes_labels_buffer,
            axes_labels_fontsize=axes_labels_fontsize,
            axes_off=axes_off,
            **text_kwargs,
        )

    # compose with existing fig if one was provided
    final_fig = fig * axis_fig if fig is not None else axis_fig

    # holoviews modification comes at the end because we modify *existing* figures with .opts()
    return _holoviews_fig_modification(
        hive_plot=hive_plot,
        fig=final_fig,
        buffer=buffer,
        width=width,
        height=height,
        center_plot=center_plot,
        axes_off=axes_off,
        overlay_kwargs=overlay_kwargs,
    )


def label_axes(
    instance: Union[HivePlot, P2CP],
    fig: Optional[hv.Overlay] = None,
    axes_labels_buffer: float = 1.1,
    axes_labels_fontsize: int = 16,
    buffer: float = 0.3,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    axes_off: bool = True,
    overlay_kwargs: Optional[dict] = None,
    **text_kwargs,
) -> hv.Overlay:
    """
    ``holoviews`` visualization of axis labels in a ``HivePlot`` or ``P2CP`` instance.

    For ``HivePlot`` instances, each axis' ``long_name`` attribute will be used. For ``P2CP`` instances, column names in
    the ``data`` attribute will be used.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw axes.
    :param fig: default ``None`` builds new overlay. If an overlay is specified, axes will be drawn on that overlay.
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for axes labels.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``instance``.
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :param text_kwargs: additional kwargs passed to
        `holoviews.Text() <https://holoviews.org/reference/elements/bokeh/Text.html>`__ call.
    :return: ``holoviews.Overlay``.
    """
    hive_plot, _, warning_raised = input_check(instance, objects_to_plot="axes")

    if warning_raised:
        return None

    label_plots = []
    for axis in hive_plot.axes.values():
        # choose horizontal and vertical alignment based on axis angle in [0, 360)
        vertical_alignment, horizontal_alignment = get_axis_label_alignment(
            axis=axis,
            backend="holoviews",
        )

        x, y = polar2cartesian(axes_labels_buffer * axis.polar_end, axis.angle)
        label = hv.Text(
            x=x,
            y=y,
            text=axis.long_name,
            fontsize=axes_labels_fontsize,
            halign=horizontal_alignment,
            valign=vertical_alignment,
            group="Labels",
        ).opts(
            **text_kwargs,
        )
        label_plots.append(label)

    labels_fig = hv.Overlay(label_plots)

    # compose with existing fig if one was provided
    final_fig = fig * labels_fig if fig is not None else labels_fig

    # holoviews modification comes at the end because we modify *existing* figures with .opts()
    return _holoviews_fig_modification(
        hive_plot=hive_plot,
        fig=final_fig,
        buffer=buffer,
        width=width,
        height=height,
        center_plot=center_plot,
        axes_off=axes_off,
        overlay_kwargs=overlay_kwargs,
    )


def node_viz(
    instance: Union[HivePlot, P2CP],
    fig: Optional[hv.Overlay] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    buffer: float = 0.3,
    axes_off: bool = True,
    overlay_kwargs: Optional[dict] = None,
    **points_kwargs,
) -> hv.Overlay:
    """
    ``holoviews`` visualization of nodes in a ``HivePlot`` or ``P2CP`` instance that have been placed on their axes.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw nodes.
    :param fig: default ``None`` builds new overlay. If an overlay is specified, axes will be drawn on that overlay.
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``instance``.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :param points_kwargs: additional params that will be applied to all hive plot nodes. Note, these are kwargs that
        affect a `holoviews.Points() <https://holoviews.org/reference/elements/matplotlib/Points.html>`__ call.
    :return: ``holoviews.Overlay``.
    """
    backend = _get_current_hv_backend()

    # some default kwargs for the nodes
    points_kwargs.setdefault("color", "black")
    points_kwargs.setdefault("alpha", 0.8)
    if backend == "bokeh":
        points_kwargs.setdefault("size", 5)
    elif backend == "matplotlib":
        points_kwargs.setdefault("s", 35)

    hive_plot, _, _ = input_check(instance, objects_to_plot="nodes")

    points_plots = []
    for axis in hive_plot.axes.values():
        to_plot = axis.node_placements.to_numpy()[:, :2]
        if to_plot.shape[0] > 0:
            pt = hv.Points(to_plot, group="Nodes").opts(**points_kwargs)
            points_plots.append(pt)

    points_fig = hv.Overlay(points_plots)

    # compose with existing fig if one was provided
    final_fig = fig * points_fig if fig is not None else points_fig

    # holoviews modification comes at the end because we modify *existing* figures with .opts()
    return _holoviews_fig_modification(
        hive_plot=hive_plot,
        fig=final_fig,
        buffer=buffer,
        width=width,
        height=height,
        center_plot=center_plot,
        axes_off=axes_off,
        overlay_kwargs=overlay_kwargs,
    )


def edge_viz(
    instance: Union[HivePlot, P2CP],
    fig: Optional[hv.Overlay] = None,
    tags: Optional[Union[Hashable, List[Hashable]]] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    buffer: float = 0.3,
    axes_off: bool = True,
    overlay_kwargs: Optional[dict] = None,
    **curve_kwargs,
) -> hv.Overlay:
    """
    ``holoviews`` visualization of constructed edges in a ``HivePlot`` or ``P2CP`` instance.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new overlay. If an overlay is specified, axes will be drawn on that overlay.
    :param tags: which tag(s) of data to plot. Default ``None`` plots all tags of data. Can supply either a single tag
        or list of tags.
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``instance``.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :param curve_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified
        beforehand in :py:meth:`hiveplotlib.HivePlot.connect_axes()` / :py:meth:`hiveplotlib.P2CP.build_edges` or
        :py:meth:`hiveplotlib.HivePlot.add_edge_kwargs()` / :py:meth:`hiveplotlib.P2CP.add_edge_kwargs()` will take
        priority). To overwrite previously set kwargs, see :py:meth:`hiveplotlib.HivePlot.add_edge_kwargs()` /
        :py:meth:`hiveplotlib.P2CP.add_edge_kwargs()` for more. Note, these are kwargs that affect a
        `holoviews.Curve() <https://holoviews.org/reference/elements/bokeh/Curve.html>`__ call.
    :return: ``holoviews.Overlay``.
    """
    backend = _get_current_hv_backend()

    hive_plot, name, warning_raised = input_check(instance, objects_to_plot="edges")

    # stop plotting if there are no edges to plot
    if warning_raised:
        return None

    if backend == "bokeh":
        line_width_name = "line_width"
    elif backend == "matplotlib":
        line_width_name = "linewidth"

    # p2cp warnings only need to happen once per tag
    #  because all axes behave in unison
    already_warned_p2cp_tags = []

    edges_plots = []

    for a0 in hive_plot.edges:
        for a1 in hive_plot.edges[a0]:
            # use all tags if no specific tags requested
            # otherwise, make sure we have a flat list of tags
            tags_to_plot = (
                hive_plot.edges[a0][a1].keys()
                if tags is None
                else list(np.array(tags).flatten())
            )

            for tag in tags_to_plot:
                temp_edge_kwargs, already_warned_p2cp_tags = edge_viz_preparation(
                    hive_plot=hive_plot,
                    name=name,
                    from_axis=a0,
                    to_axis=a1,
                    tag=tag,
                    already_warned_p2cp_tags=already_warned_p2cp_tags,
                    edge_kwargs=curve_kwargs,
                    line_width_name=line_width_name,
                    line_alpha_name="alpha",
                    line_color_name="color",
                )

                # only run plotting of edges that exist
                if "curves" in hive_plot.edges[a0][a1][tag]:
                    # grab the requested array of discretized curves
                    edge_arr = hive_plot.edges[a0][a1][tag]["curves"]
                    # if there's no actual edges there, don't plot
                    if edge_arr.size > 0:
                        split_arrays = np.split(
                            edge_arr, np.where(np.isnan(edge_arr[:, 0]))[0]
                        )
                        temp_curves = hv.Path(
                            split_arrays,
                            group="edges",
                            label=f"{tag}",  # tag labels must be strings
                        ).opts(
                            **hive_plot.edges[a0][a1][tag]["edge_kwargs"],
                            **temp_edge_kwargs,
                        )
                        edges_plots.append(temp_curves)

    edges_fig = hv.Overlay(edges_plots)

    # compose with existing fig if one was provided
    final_fig = fig * edges_fig if fig is not None else edges_fig

    # holoviews modification comes at the end because we modify *existing* figures with .opts()
    return _holoviews_fig_modification(
        hive_plot=hive_plot,
        fig=final_fig,
        buffer=buffer,
        width=width,
        height=height,
        center_plot=center_plot,
        axes_off=axes_off,
        overlay_kwargs=overlay_kwargs,
    )


def hive_plot_viz(
    hive_plot: HivePlot,
    fig: Optional[hv.Overlay] = None,
    tags: Optional[Union[Hashable, List[Hashable]]] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    buffer: float = 0.3,
    show_axes_labels: bool = True,
    axes_labels_buffer: float = 1.1,
    axes_labels_fontsize: int = 16,
    axes_off: bool = True,
    node_kwargs: Optional[dict] = None,
    axes_kwargs: Optional[dict] = None,
    text_kwargs: Optional[dict] = None,
    overlay_kwargs: Optional[dict] = None,
    **edge_kwargs,
) -> hv.Overlay:
    """
    Create default ``holoviews`` visualization of a ``HivePlot`` instance.

    :param hive_plot: ``HivePlot`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new overlay. If an overlay is specified, axes will be drawn on that overlay.
    :param tags: which tag(s) of data to plot. Default ``None`` plots all tags of data. Can supply either a single tag
        or list of tags.
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``hive_plot``.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for hive plot axes labels.
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param node_kwargs: additional params that will be applied to all hive plot nodes. Note, these are kwargs that
        affect a `holoviews.Points() <https://holoviews.org/reference/elements/matplotlib/Points.html>`__ call.
    :param axes_kwargs: additional params that will be applied to all hive plot axes. Note, these are kwargs that
        affect a `holoviews.Curve() <https://holoviews.org/reference/elements/bokeh/Curve.html>`__ call.
    :param text_kwargs: additional kwargs passed to
        `holoviews.Text() <https://holoviews.org/reference/elements/bokeh/Text.html>`__ call.
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified
        beforehand in :py:meth:`hiveplotlib.HivePlot.connect_axes()` or
        :py:meth:`hiveplotlib.HivePlot.add_edge_kwargs()` will take priority). To overwrite previously set kwargs, see
        :py:meth:`hiveplotlib.HivePlot.add_edge_kwargs()` for more. Note, these are kwargs that affect a
        `holoviews.Curve() <https://holoviews.org/reference/elements/bokeh/Curve.html>`__ call.
    :return: ``holoviews.Overlay``.
    """
    if node_kwargs is None:
        node_kwargs = {}

    if axes_kwargs is None:
        axes_kwargs = {}

    fig = edge_viz(
        instance=hive_plot,
        fig=fig,
        tags=tags,
        center_plot=False,
        **edge_kwargs,
    )

    fig = axes_viz(
        instance=hive_plot,
        fig=fig,
        center_plot=False,
        show_axes_labels=show_axes_labels,
        axes_labels_buffer=axes_labels_buffer,
        axes_labels_fontsize=axes_labels_fontsize,
        text_kwargs=text_kwargs,
        **axes_kwargs,
    )

    # do the centering / redim-ing if requested only on the last call, otherwise it will be overridden
    return node_viz(
        instance=hive_plot,
        fig=fig,
        width=width,
        height=height,
        buffer=buffer,
        center_plot=center_plot,
        axes_off=axes_off,
        overlay_kwargs=overlay_kwargs,
        **node_kwargs,
    )


def p2cp_viz(
    p2cp: P2CP,
    fig: Optional[hv.Overlay] = None,
    tags: Optional[Union[Hashable, List[Hashable]]] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    center_plot: bool = True,
    buffer: float = 0.3,
    show_axes_labels: bool = True,
    axes_labels_buffer: float = 1.1,
    axes_labels_fontsize: int = 16,
    axes_off: bool = True,
    node_kwargs: Optional[dict] = None,
    axes_kwargs: Optional[dict] = None,
    text_kwargs: Optional[dict] = None,
    overlay_kwargs: Optional[dict] = None,
    **edge_kwargs,
) -> hv.Overlay:
    """
    Create default ``holoviews`` visualization of a ``P2CP`` instance.

    :param p2cp: ``P2CP`` instance we want to visualize.
    :param fig: default ``None`` builds new overlay. If an overlay is specified, axes will be drawn on that overlay.
    :param tags: which tag(s) of data to plot. Default ``None`` plots all tags of data. Can supply either a single tag
        or list of tags.
    :param width: width of figure. When the ``holoviews`` backend is set to ``"bokeh"``, width must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, width must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param height: height of figure. When the ``holoviews`` backend is set to ``"bokeh"``, height must be specified in
        *pixels*, defaulting to 600. When the ``holoviews`` backend is set to ``"matplotlib"``, height must be specified
        in *inches*, defaulting to 10. Note: only works if instantiating new figure (e.g. ``fig`` is ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that the axes are drawn
        around by default. Will only run if there is at least one axis in ``p2cp``.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g. setting ``buffer`` will
        find the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``).
    :param show_axes_labels: whether to label the P2CP axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for P2CP axes labels.
    :param axes_off: whether to turn off Cartesian x, y axes in the ``hv.Overlay`` (default ``True`` hides the x and y
        axes).
    :param node_kwargs: additional params that will be applied to all P2CP nodes. Note, these are kwargs that
        affect a `holoviews.Points() <https://holoviews.org/reference/elements/matplotlib/Points.html>`__ call.
    :param axes_kwargs: additional params that will be applied to all P2CP axes. Note, these are kwargs that
        affect a `holoviews.Curve() <https://holoviews.org/reference/elements/bokeh/Curve.html>`__ call.
    :param text_kwargs: additional kwargs passed to
        `holoviews.Text() <https://holoviews.org/reference/elements/bokeh/Text.html>`__ call.
    :param overlay_kwargs: additional values to be called in ``hv.Overlay().opts()`` call. Note if ``width`` and
        ``height`` are added here, then they will be prioritized over the ``width`` and ``height`` parameters.
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified beforehand
        in :py:meth:`hiveplotlib.P2CP.build_edges()` or :py:meth:`hiveplotlib.P2CP.add_edge_kwargs()` will
        take priority). To overwrite previously set kwargs, see :py:meth:`hiveplotlib.P2CP.add_edge_kwargs()` for more.
        Note, these are kwargs that affect a
        `holoviews.Curve() <https://holoviews.org/reference/elements/bokeh/Curve.html>`__ call.
    :return: ``holoviews.Overlay``.
    """
    if node_kwargs is None:
        node_kwargs = {}

    if axes_kwargs is None:
        axes_kwargs = {}

    fig = edge_viz(
        instance=p2cp,
        fig=fig,
        tags=tags,
        center_plot=False,
        **edge_kwargs,
    )

    fig = axes_viz(
        instance=p2cp,
        fig=fig,
        center_plot=False,
        show_axes_labels=show_axes_labels,
        axes_labels_buffer=axes_labels_buffer,
        axes_labels_fontsize=axes_labels_fontsize,
        text_kwargs=text_kwargs,
        **axes_kwargs,
    )

    # do the centering / redim-ing if requested only on the last call, otherwise it will be overridden
    return node_viz(
        instance=p2cp,
        fig=fig,
        width=width,
        height=height,
        buffer=buffer,
        center_plot=center_plot,
        axes_off=axes_off,
        overlay_kwargs=overlay_kwargs,
        **node_kwargs,
    )


def p2cp_legend(
    fig: hv.Overlay,
    **legend_kwargs,
) -> hv.Overlay:
    """
    Generate a legend for a ``P2CP`` instance, where entries in the legend will be tags of data added to the instance.

    :param p2cp: ``P2CP`` instance we want to visualize.
    :param fig: ``plotly`` figure on which we will draw the legend.
    :param legend_kwargs: additional values to be called in ``hv.Overlay().opts()`` call.
    :return: ``holoviews.Overlay``.
    """
    return fig.opts(hv.opts.Path(show_legend=True), **legend_kwargs)
