amen_list = ['Amenities', 'Retail/Restaurants', 'Location','Sustainabiliy', 'Maintenance', 'Security', 'Other']
color_select = '#f67171'
color_compare = '#bfbfbf'
import matplotlib.pyplot as plt
import numpy as np


def draw_user_for_selection(df, color):
    data_eng = df[['April', 'May', 'June']]
    data_forecast = df[['April', 'May', 'June', 'July (forecast)']]
    plot_1_1 = data_eng.mean().hvplot(ylim = (0,100), line_color=color, 
        line_width=4, legend = False).opts(toolbar='disable')
    plot_1_2 = data_forecast.mean().hvplot(ylim = (0,100), line_color=color, line_dash = 'dashed', line_width=4, 
        legend = False).opts(title = 'Users across the app (percentage of building population)', 
        yformatter= "%.0f%%", width = 400, toolbar='disable', xlabel = ' ')
    plot_1_3 = data_forecast.mean().hvplot(color=color, kind='scatter', legend = False, s=75)
    p = plot_1_2 * plot_1_1 * plot_1_3
    return p

def draw_user_compare(df, color):
    plot_1_1 = df[['April', 'May', 'June']].mean().hvplot(line_color=color, 
        line_width=4, legend = False).opts(toolbar='disable')
    plot_1_2 = df[['April', 'May', 'June', 'July (forecast)']].mean().hvplot(line_color=color, 
        line_dash = 'dashed', line_width=4, legend = False).opts(toolbar='disable')
    plot_1_3 = df[['April', 'May', 'June', 'July (forecast)']].mean().to_frame().rename(columns = /
        {0: 'Selected Building'}).hvplot(color=color, kind='scatter', s=75).opts(toolbar='disable' )

    p = plot_1_2 * plot_1_1 * plot_1_3
    return p


def draw_amen_selection(df, color):
    amen_data = df[amen_list]

    if len(df) < 2:
        g = amen_data.hvplot(kind = 'bar', color=color, legend = False).opts(title = 'User selected amenities ', 
            yformatter= "%.0f%%", width = 400, toolbar='disable', xrotation=12, xlabel = ' ')
        return g
    if color == color_compare:
        g = amen_data.hvplot.box(color=color, legend = False , alpha=0.2).opts(whisker_color='gray',
            box_line_color='gray', outlier_color = 'white', title = 'User selected amenities ', 
            yformatter= "%.0f%%", width = 400, toolbar='disable', xrotation=12, xlabel=' ')  
        return g

    g = amen_data.hvplot.box(color=color, legend = False).opts(title = 'User selected amenities ', 
    yformatter= "%.0f%%", width = 400, toolbar='disable', xrotation=12, xlabel = ' ')    
    return g


def draw_amen_compare(df, color):
    amen_data_x = df[amen_list]
    amen_data_x = amen_data_x.mean().to_frame()
    for i in range(10):
        amen_data_x[str(i)] = amen_data_x[0] + (i*0.33)
    g = amen_data_x.hvplot(kind = 'scatter', marker='dash', s=1800, color=color, 
        legend = False).opts(toolbar='disable')
    return g

def polar_plot(polar_df):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="polar")

    # theta has len(d) different angles, and the first one repeated
    theta = np.arange(len(polar_df) + 1) / float(len(polar_df)) * 2 * np.pi
    theta += np.pi/2
    values = polar_df['Col B'].values
    values = np.append(values, values[0])

    l1, = ax.plot(theta, values, color='#f08a67',markersize=8, marker="o",linewidth=4, label="Name of Col B");
    ax.set_ylim(0,1)
    ax.set_thetagrids([(x*57.2958)%360 for x in theta[:-1]], list(polar_df['Col A'].values));
    ax.set_rgrids([.25,.5,.75],[]);
    ax.tick_params(pad=5);

    ax.fill(theta, values, '#f67171', alpha=0.1);

    return fig