import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation

# pycharm animation support
matplotlib.use("TkAgg")


class Graph:
    # red, maroon, yellow, forest, blue, cyan, darkpink
    colors = ['#e83b3b', '#7a3045', '#f9c22b', '#165a4c', '#4d9be6', '#30e1b9', '#c32454']

    @staticmethod
    def plot_animated(data):
        # forgive me
        fig, ax = plt.subplots(figsize=(8, 4))

        lines = []
        scatters = []
        start_scatters = []

        for i in range(data.settings.agents):
            current_color = Graph.colors[i % 8]
            flight_path_line, = ax.plot([], [], lw=2, color=current_color, linestyle='--')
            # reshape color here but whatevs
            scatter = ax.scatter([], [], marker='o', c=current_color, s=50)

            start_pos = data.agents[i]["position_history"][0]
            # reshape this too
            start_scatter = ax.scatter(start_pos[0], start_pos[1], alpha=0.5, color=current_color, s=100, marker='o',
                                       label=f'Drone {i + 1}')

            lines.append(flight_path_line)
            scatters.append(scatter)
            start_scatters.append(start_scatter)

        # reshape this color too maybe
        goal_scatter = ax.scatter([], [], c="#2e222f", marker='$*$', s=100, label="Target")
        goal_scatter.set_offsets([data.settings.goal_x, data.settings.goal_y])

        def init():
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            if not data.settings.follow_agents:
                ax.set_ylim(data.settings.y_min, data.settings.y_max)
                ax.set_xticks(range(data.settings.x_min, data.settings.x_max, data.settings.x_ticks))
            else:
                ax.set_aspect('equal', adjustable='datalim')

            for dashed_line, scatter in zip(lines, scatters):
                dashed_line.set_data([], [])
                scatter.set_offsets(np.empty((0, 2)))
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=handles, labels=labels, loc="upper left", labelspacing=0.6, fontsize=10)
            return lines + scatters + start_scatters

        def animate(frame):
            for i, (dashed_line, scatter) in enumerate(zip(lines, scatters)):
                all_positions = data.agents[i]["position_history"]

                dashed_line.set_data([x for x, y in all_positions[:frame + 1]],
                                     [y for x, y in all_positions[:frame + 1]])
                start_x, start_y = all_positions[frame]
                scatter.set_offsets([start_x, start_y])
            if frame == data.settings.rounds - 1:
                plt.savefig(f'{data.directory}/last.svg', bbox_inches='tight')

            return lines + scatters

        ani = FuncAnimation(fig, animate, frames=data.settings.rounds, init_func=init, blit=False)
        ani.save(f'{data.directory}/animation.gif', fps=20)
        plt.show()
