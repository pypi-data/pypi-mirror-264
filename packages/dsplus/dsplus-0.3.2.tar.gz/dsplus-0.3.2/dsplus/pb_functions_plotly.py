#region Libraries

#%%
from typing import Literal, Self, Any

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio

#endregion -----------------------------------------------------------------------------------------
#region Functions

#%%
def px_add_trace_data(fig_original, *figs):
    # TODO not working (only takes first fig)
    for fig in figs:
        if fig_original is not None:
            for i in range(len(fig.data)):
                fig_original.add_trace(fig.data[i])
        else:
            fig_original = fig
        return fig_original

#endregion -----------------------------------------------------------------------------------------
#region Class

#%%
class px_Plot():
    fig = None
    df = None
    facet_flag = False
    facet_row = None
    facet_col = None
    facet_row_spacing = None
    facet_col_spacing = None
    facet_n_col = 0
    category_orders = None
    facet_x_show_labels = False
    facet_y_show_labels = False
    facet_x_free = False
    facet_y_free = False
    marginal_x = None
    marginal_y = None
    marginal_xy = None
    x_log = False
    y_log = False

    def __init__(self,
                 df: pd.DataFrame=None,
                 x=None,
                 y=None) -> None:
        # fig = px.scatter()

        if df is not None:
            self.df = df.copy()
        self.x = x
        self.y = y
        # self.fig = fig

    def facet(self,
              row=None,
              col=None,
              row_spacing=None,
              col_spacing=None,
              n_col=None,
              x_show_labels=False,
              y_show_labels=False,
              x_free=False,
              y_free=False,
              row_order=None,
              col_order=None):
        if row_order is not None:
            row_order = {row: row_order}
        else:
            row_order = {}
        if col_order is not None:
            col_order = {col: col_order}
        else:
            col_order = {}
        category_orders = row_order | col_order

        if x_free == True:
            x_show_labels = True
        if y_free == True:
            y_show_labels = True

        if row is not None and col is None:
            row, col = None, row

        self.facet_flag=True
        self.facet_row=row
        self.facet_col=col
        self.facet_row_spacing=row_spacing
        self.facet_col_spacing=col_spacing
        self.facet_n_col=n_col
        self.category_orders = category_orders
        self.facet_x_show_labels = x_show_labels
        self.facet_y_show_labels = y_show_labels
        self.facet_x_free = x_free
        self.facet_y_free = y_free

        return self

    def marginal(self,
                 x=None,
                 y=None):
        marginal_xy=x if x is not None else y

        self.marginal_x = x
        self.marginal_y = y
        self.marginal_xy = marginal_xy

        return self

    def transform(self,
                  x_log = False,
                  y_log = False):
        self.x_log = x_log
        self.y_log = y_log

        return self

    def _update_facet_axes(self):
        if self.facet_flag:
            if self.facet_x_show_labels:
                self.fig.update_xaxes(showticklabels=True)
            if self.facet_y_show_labels:
                self.fig.update_yaxes(showticklabels=True)
            if self.facet_x_free:
                self.fig.update_xaxes(matches=None)
            if self.facet_y_free:
                self.fig.update_yaxes(matches=None)

    def _update_legend_show(self, trace, legend_show, legend_name):
        if legend_show is not None:
            trace.update_traces(showlegend=legend_show)
        if legend_name is not None:
            trace.update_traces(name=legend_name)

    def dec_add(marginal='xy'):
        '''Decorator to make the following updates:
            -  
        '''
        def inner(func):
            def wrapper(self, *args, **kwargs):
                if kwargs.get('category_orders') is not None or self.category_orders is not None:
                    kwargs['category_orders']=({} if kwargs.get('category_orders') is None else kwargs.get('category_orders')) | ({} if self.category_orders is None else self.category_orders)
                else:
                    kwargs['category_orders']=self.category_orders
                
                kwargs['facet_row']=self.facet_row
                kwargs['facet_col']=self.facet_col
                kwargs['facet_col_wrap']=self.facet_n_col
                kwargs['facet_row_spacing']=self.facet_row_spacing
                kwargs['facet_col_spacing']=self.facet_col_spacing
                kwargs['log_x']=self.x_log
                kwargs['log_y']=self.y_log

                kwargs |= {d.replace('aes_', ''):kwargs[d] for d in kwargs if d.startswith('aes_')}

                _ = dict()

                if kwargs.get('df') is None:
                    _['data_frame'] = self.df.copy()
                elif 'df' in kwargs:
                    _['data_frame'] = kwargs.pop('df')
                if kwargs.get('x') is None:
                    _['x'] = self.x
                elif 'x' in kwargs:
                    _['x'] = kwargs.pop('x')
                if kwargs.get('y') is None:
                    _['y'] = self.y
                elif 'y' in kwargs:
                    _['y'] = kwargs.pop('y')

                for name in ['category_orders', 'hover_name', 'hover_data', 'animation_frame', 'animation_group']:
                    if name in kwargs:
                        _[name] = kwargs.pop(name)

                kwargs['_'] = _

                if marginal == 'xy':
                    kwargs['marginal_x']=self.marginal_x
                    kwargs['marginal_y']=self.marginal_y
                elif marginal == '':
                    pass
                else:
                    kwargs['marginal']=self.marginal_xy

                # return func(self, *args, **kwargs)
                    
                trace = func(self, *args, **kwargs)

                self._update_legend_show(trace, kwargs.get('legend_show'), kwargs.get('legend_name'))
                
                self.add(trace)
                
                self._update_facet_axes()
                
                return self
            
            return wrapper
        return inner

    def add(self,
            trace,
            df:pd.DataFrame=None):
        fig = self.fig

        fig = px_add_trace_data(fig, trace)

        self.fig=fig
        return self

    @dec_add(marginal='xy')
    def add_scatter(self,
                    df: pd.DataFrame = None,
                    x = None,
                    y = None,
                    color = None,
                    size = None,
                    symbol = None,
                    opacity = None,
                    color_value = None,
                    size_value = None,
                    symbol_value = None,
                    color_line_value = None,
                    width_line_value = None,
                    opacity_value = None,
                    aes_color_discrete_sequence = None,
                    aes_color_discrete_map = None,
                    aes_color_continuous_scale = None,
                    aes_range_color = None,
                    aes_color_continuous_midpoint = None,
                    aes_symbol_sequence = None,
                    aes_symbol_map = None,
                    aes_size_max = None,                    
                    text = None,
                    text_position: Literal['top left', 'top center', 'top right', 
                                           'middle left', 'middle center', 'middle right', 
                                           'bottom left', 'bottom center', 'bottom right'] = None,
                    category_orders = None,
                    legend_show = None,
                    legend_name = None,
                    hover_name = None,
                    hover_data = None,
                    hover_template = None,
                    animation_frame = None,
                    animation_group = None,
                    _ = None,
                    **kwargs) -> Self:
        trace = \
        (px.scatter(
            color=color,
            size=size,
            symbol=symbol,
            opacity=opacity,
            text=text,
            **_,
            **kwargs
            )
            .update_traces(marker_line_color=color_line_value,
                           marker_line_width=width_line_value)
        )
        if kwargs.get('marginal_x') is None and kwargs.get('marginal_y') is None:
            trace.update_traces(textposition=text_position)
        if color_value is not None:
            trace.update_traces(marker_color=color_value)
        if size_value is not None:
            trace.update_traces(marker_size=size_value)
        if symbol_value is not None:
            trace.update_traces(marker_symbol=symbol_value)
        if opacity_value is not None:
            trace.update_traces(marker_opacity=opacity_value)
        if hover_template is not None:
            trace.update_traces(hovertemplate=hover_template)

        return trace

    @dec_add(marginal='')
    def add_line(self,
                 df: pd.DataFrame = None,
                 x = None,
                 y = None,
                 color = None,
                 dash = None,
                 color_value = None,
                 width_value = None,
                 shape_value = None,
                 dash_value = None,
                 opacity_value = None,
                 aes_color_discrete_sequence = None,
                 aes_color_discrete_map = None,
                 line_dash_sequence = None,
                 line_dash_map = None,
                 symbol_sequence = None,
                 symbol_map = None,
                 text = None,
                 text_position: Literal['top left', 'top center', 'top right', 
                                        'middle left', 'middle center', 'middle right', 
                                        'bottom left', 'bottom center', 'bottom right'] = None,
                 category_orders = None,
                 legend_show = None,
                 legend_name = None,
                 hover_name = None,
                 hover_data = None,
                 hover_template = None,
                 animation_frame = None,
                 animation_group = None,
                 _ = None,
                 **kwargs) -> Self:
        trace = \
        (px.line(
            color=color,
            line_dash=dash,
            text=text,
            **_,
            **kwargs
            )
            .update_traces(line_width=width_value,
                           line_shape=shape_value,
                           opacity=opacity_value,
                           textposition=text_position)
        )
        if color_value is not None:
            trace.update_traces(line_color=color_value)
        if dash_value is not None:
            trace.update_traces(line_dash=dash_value)
        if hover_template is not None:
            trace.update_traces(hovertemplate=hover_template)
        
        return trace

    @dec_add(marginal='')
    def add_bar(self,
                 df: pd.DataFrame = None,
                 x = None,
                 y = None,
                 color = None,
                 pattern = None,
                 color_value = None,
                 color_line_value = None,
                 width_line_value = None,
                 opacity_value = None,
                 aes_color_discrete_sequence = None,
                 aes_color_discrete_map = None,
                 aes_pattern_shape_sequence = None,
                 aes_pattern_shape_map = None,
                 aes_range_color = None,
                 aes_color_continuous_midpoint = None,
                 bar_mode: Literal['group', 'overlay', 'relative'] = 'relative',
                 bar_gap = None,
                 text = None,
                 text_position: Literal['top left', 'top center', 'top right', 
                                        'middle left', 'middle center', 'middle right', 
                                        'bottom left', 'bottom center', 'bottom right'] = None,
                 category_orders = None,
                 legend_show = None,
                 legend_name = None,
                 hover_name = None,
                 hover_data = None,
                 hover_template = None,
                 animation_frame = None,
                 animation_group = None,
                 _ = None,
                 **kwargs) -> Self:
        if df is None:
            df = self.df.copy()
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        trace = \
        (px.bar(
            color=color,
            pattern_shape=pattern,
            barmode=bar_mode,
            text=text,
            **_,
            **kwargs
            )
            .update_traces(marker_line_color=color_line_value,
                           marker_line_width=width_line_value,
                           textposition=text_position)
            .update_layout(bargap=bar_gap)
        )
        if color_value is not None:
            trace.update_traces(marker_color=color_value)
        if opacity_value is not None:
            trace.update_traces(marker_opacity=opacity_value)
        if hover_template is not None:
            trace.update_traces(hovertemplate=hover_template)

        return trace

    @dec_add(marginal='x')
    def add_histogram(self,
                      df: pd.DataFrame = None,
                      x = None,
                      y = None,
                      color = None,
                      shape = None,
                      color_value = None,
                      color_line_value = None,
                      width_line_value = None,
                      opacity_value = None,
                      aes_color_discrete_sequence = None,
                      aes_color_discrete_map = None,
                      aes_pattern_shape_sequence = None,
                      aes_pattern_shape_map = None,
                      text_auto = False,
                      bins_n = None,
                      bins_start = None,
                      bins_end = None,
                      bins_size = None,
                      cumulative = False,
                      hist_func: Literal['count', 'sum', 'avg', 'min', 'max'] = None,
                      hist_norm: Literal['percent', 'probability', 'density', 'probability density'] = None,
                      bar_mode: Literal['group', 'overlay', 'relative'] = 'relative',
                      bar_norm: Literal['fraction', 'percent'] = None,
                      bar_gap = None,
                      category_orders = None,
                      legend_show = None,
                      legend_name = None,
                      hover_name = None,
                      hover_data = None,
                      hover_template = None,
                      animation_frame = None,
                      animation_group = None,
                      _ = None,
                      **kwargs) -> Self:
        if hist_func is None:
            hist_func = 'count' if y is None else 'sum'

        trace = \
        (px.histogram(
            color=color,
            pattern_shape=shape,
            text_auto=text_auto,
            nbins=bins_n,
            cumulative=cumulative,
            histfunc=hist_func,
            histnorm=hist_norm,
            barmode=bar_mode,
            barnorm=bar_norm,
            **_,
            **kwargs
            )
            .update_traces(marker_line_color=color_line_value,
                           marker_line_width=width_line_value)
            .update_layout(bargap=bar_gap)
        )
        if kwargs.get('marginal') is None: # Is this a plotly express bug?
            trace.update_traces(xbins = dict(start = bins_start,
                                             end = bins_end,
                                             size = bins_size))
            
        if color_value is not None:
            trace.update_traces(marker_color=color_value)
        if opacity_value is not None:
            trace.update_traces(marker_opacity=opacity_value)
        if hover_template is not None:
            trace.update_traces(hovertemplate=hover_template)

        return trace
    
    @dec_add(marginal='xy')
    def add_heatmap(self,
                    df: pd.DataFrame = None,
                    x = None,
                    y = None,
                    z = None,
                    opacity_value = None,
                    aes_color_continuous_scale = None,
                    aes_range_color = None,
                    color_continuous_midpoint = None,
                    text_auto = False,
                    bins_n_x = None,
                    bins_start_x = None,
                    bins_end_x = None,
                    bins_size_x = None,
                    bins_n_y = None,
                    bins_start_y = None,
                    bins_end_y = None,
                    bins_size_y = None,
                    hist_func: Literal['count', 'sum', 'avg', 'min', 'max'] = None,
                    hist_norm: Literal['percent', 'probability', 'density', 'probability density'] = None,
                    bar_mode: Literal['group', 'overlay', 'relative'] = 'relative',
                    bar_norm: Literal['fraction', 'percent'] = None,
                    bar_gap = None,
                    category_orders = None,
                    legend_show = None,
                    legend_name = None,
                    hover_name = None,
                    hover_data = None,
                    hover_template = None,
                    animation_frame = None,
                    animation_group = None,
                    _ = None,
                    **kwargs) -> Self:
        if hist_func is None:
            hist_func = 'count' if z is None else 'sum'
        
        trace = \
        (px.density_heatmap(
            z=z,
            text_auto=text_auto,
            nbinsx=bins_n_x,
            nbinsy=bins_n_y,
            histfunc=hist_func,
            histnorm=hist_norm,
            **_,
            **kwargs
            )
        )
        if kwargs.get('marginal_x') is None and kwargs.get('marginal_y') is None: # Is this a plotly express bug?
            trace.update_traces(xbins = dict(start = bins_start_x,
                                             end = bins_end_x,
                                             size = bins_size_x),
                                ybins = dict(start = bins_start_y,
                                             end = bins_end_y,
                                             size = bins_size_y))
            
        if opacity_value is not None:
            trace.update_traces(marker_opacity=opacity_value)
        if hover_template is not None:
            trace.update_traces(hovertemplate=hover_template)

        return trace
    
    #TODO facet
    def add_kde(self,
                df: pd.DataFrame = None,
                x = None,
                color_value = None,
                width_value = None,
                dash_value = None,
                legend_show = None,
                legend_name = None):
        facet_row=self.facet_row
        facet_col=self.facet_col
        facet_row_spacing=self.facet_row_spacing
        facet_col_spacing=self.facet_col_spacing
        facet_n_col=self.facet_n_col
        category_orders=self.category_orders
        x_log=self.x_log
        y_log=self.y_log

        if df is None:
            df = self.df.copy()
        if x is None:
            x = self.x

        trace = \
        (ff.create_distplot([df[x].tolist()], 
                               [x], 
                               show_hist=False, 
                               show_rug=False)        
            .update_traces(line_color=color_value,
                           line_width=width_value,
                           line_dash=dash_value)
            .update_traces(showlegend=False)
        )

        self._update_legend_show(trace, legend_show, legend_name)

        self.add(trace)

        self._update_facet_axes()

        return self

    def label(self,
              x = None,
              y = None,
              title = None,
              x_tickformat = None,
              y_tickformat = None,
              title_x_just = None):
        fig = self.fig

        fig.update_layout(xaxis_title = x,
                          yaxis_title = y,
                          title = title)

        fig.update_xaxes(tickformat=x_tickformat)
        fig.update_yaxes(tickformat=y_tickformat)
        fig.update_layout(title_x=title_x_just)

        return self

    def legend(self,
               show = True,
               title = None,
               x_anchor: Literal['auto', 'left', 'center', 'right'] = None,
               y_anchor: Literal['auto', 'top', 'middle', 'bottom'] = None,
               x = None,
               y = None,
               orientation = None):
        fig = self.fig

        fig.update_layout(showlegend = show,
                          legend = dict(title=title,
                                        xanchor=x_anchor,
                                        yanchor=y_anchor,
                                        x = x,
                                        y = y,
                                        orientation = orientation))

        return self

    def colorbar(self,
                 show = True,
                 title = None,
                 x_anchor = None,
                 y_anchor = None,
                 x = None,
                 y = None,
                 orientation = None,
                 thickness = None,
                 len = len):
        fig = self.fig

        fig.update_layout(showlegend = show,
                          coloraxis_colorbar=dict(title=title,
                                                  xanchor=x_anchor,
                                                  yanchor=y_anchor,
                                                  x = x,
                                                  y = y,
                                                  orientation = orientation,
                                                  thickness=thickness,
                                                  len=len))

        return self

    def size(self,
             width=None,
             height=None):
        fig = self.fig

        fig.update_layout(width=width,
                          height=height)

        return self

    def _update_axis(self,
                     axis='x',
                     kwargs=None):
        fig = self.fig

        kwargs = dict(showgrid = kwargs['tick_show_grid'],
                      zeroline = kwargs['tick_show_zero_line'],
                      showticklabels = kwargs['tick_show_labels'],
                      tick0 = kwargs['tick_0'],
                      dtick = kwargs['tick_del'],
                      ticklabelstep = kwargs['tick_label_step'],
                      nticks = kwargs['tick_n'],
                      tickangle = kwargs['tick_angle'],
                      minor_showgrid = kwargs['minor_tick_show_grid'],
                      minor_tickcolor = kwargs['minor_tick_color'],
                      minor_ticklen = kwargs['minor_tick_len'],
                      minor_griddash = kwargs['minor_tick_dash'],
                      showline = kwargs['border_show'],
                      linewidth = kwargs['border_width'],
                      linecolor = kwargs['border_color'],
                      mirror = kwargs['border_mirror'],
                      range = kwargs['value_range'],
                      categoryorder = kwargs.get('category_order'),
                      autorange = None if kwargs['value_rev'] is None else 'reversed')

        if axis=='x':
            fig.update_xaxes(**kwargs)
        elif axis=='y':
            fig.update_yaxes(**kwargs)
        else:
            fig.update_xaxes(**kwargs)
            fig.update_yaxes(**kwargs)

    def axis(self,
             tick_show_grid=None,
             tick_show_zero_line=None,
             tick_show_labels=None,
             tick_0=None,
             tick_del=None,
             tick_label_step=None,
             tick_n=None,
             tick_angle=None,
             minor_tick_show_grid=None,
             minor_tick_color=None,
             minor_tick_len=None,
             minor_tick_dash=None,
             border_show=None,
             border_width=None,
             border_color=None,
             border_mirror=None,
             aspect_ratio=None,
             value_range=None,
             value_rev=None):
        self._update_axis('both', locals())
        fig = self.fig

        if aspect_ratio is not None:
            fig.update_yaxes(scaleratio = aspect_ratio,
                             scaleanchor = 'x')

        return self

    def axis_x(self,
               tick_show_grid=None,
               tick_show_zero_line=None,
               tick_show_labels=None,
               tick_0=None,
               tick_del=None,
               tick_label_step=None,
               tick_n=None,
               tick_angle=None,
               minor_tick_show_grid=None,
               minor_tick_color=None,
               minor_tick_len=None,
               minor_tick_dash=None,
               border_show=None,
               border_width=None,
               border_color=None,
               border_mirror=None,
               value_range=None,
               value_rev=None,
               category_order=None):
        self._update_axis('x', locals())

        return self

    def axis_y(self,
               tick_show_grid=None,
               tick_show_zero_line=None,
               tick_show_labels=None,
               tick_0=None,
               tick_del=None,
               tick_label_step=None,
               tick_n=None,
               tick_angle=None,
               minor_tick_show_grid=None,
               minor_tick_color=None,
               minor_tick_len=None,
               minor_tick_dash=None,
               border_show=None,
               border_width=None,
               border_color=None,
               border_mirror=None,
               value_range=None,
               value_rev=None,
               category_order=None):
        self._update_axis('y', locals())

        return self

    def layout(self,
               margin_l = None,
               margin_r = None,
               margin_t = None,
               margin_b = None,
               scatter_mode: Literal['overlay', 'group'] = None,
               scatter_gap: float = None,
               **kwargs):
        fig = self.fig

        fig.update_layout(margin_l=margin_l,
                          margin_r=margin_r,
                          margin_t=margin_t,
                          margin_b=margin_b,
                          scattermode=scatter_mode,
                          scattergap=scatter_gap,
                          **kwargs)

        return self

    def show(self) -> None:
        fig = self.fig

        fig.show()

    def get_fig(self):
        fig = self.fig

        return fig

#endregion -----------------------------------------------------------------------------------------
