def create_visualization_plot(original_data, modeling_data, crack_analysis, output_file, optimal_span, file_no_txt):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(60, 24))
    if not crack_analysis.empty:
        ax.scatter(crack_analysis['mid.x'], crack_analysis['min.z'], c='#53868B', marker='o', s=100, label='Crack Midpoints (X,Z)', zorder = 3)
    ax.scatter(original_data['x'], original_data['pred'], c='#8EE5EE', s=5, label='Spline Fit of Original Line Scan', zorder = 3)
    ax.scatter(original_data['x'], original_data['z'], c='#BFBFBF', label='Original Data', alpha=0.6, zorder = 1)
    ax.scatter(modeling_data['x'], modeling_data['z'], c='#999999', label='Modeling Data Profile', alpha=0.6, zorder = 2)
    ax.set_xlabel('Sample Width (mm)')
    ax.set_ylabel('Relative Sample Depth (μm)')
    ax.set_title(f'Surface Spline and Calculated Crack Locations ({file_no_txt})')
    ax.legend()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_depth_plot(data, output_file, title):
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(30, 12))
    if not data.empty:
        data.plot.kde(ax=ax, linewidth=1.5, color='#1f77b4', alpha=0.4)
    ax.set_xlabel('Crack Depth (μm)')
    ax.set_ylabel('Density')
    ax.set_title(title)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_width_plot(data, output_file, title):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(30, 12))
    if not data.empty:
        data.plot.kde(ax=ax, linewidth=1.5, color='#1f77b4', alpha=0.4)
    ax.set_xlabel('Crack Width (μm)')
    ax.set_ylabel('Density')
    ax.set_title(title)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_baseline_plot(original_data, modeling_data, crack_analysis, output_file, file_no_txt):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(60, 24))
    if not crack_analysis.empty:
        ax.scatter(crack_analysis['mid.x'], crack_analysis['depth'], c='#53868B', marker='o', s=100, label='Crack Midpoints', zorder = 2)
    ax.scatter(original_data['x'], original_data['resid'], c='#BFBFBF', s=5, label='Original Data (Baselined)', zorder = 1)
    ax.scatter(modeling_data['x'], modeling_data['resid'], c='#999999', s=5, label='Modeling Data (Baselined)', zorder = 2)
    ax.set_xlabel('Sample Width (mm)')
    ax.set_ylabel('Relative Sample Depth (μm)')
    ax.set_title(f'Baselined Data ({file_no_txt})')
    ax.legend()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()