from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


def get_derivative(state, t, l1, l2, m1, m2):
    g = 9.8
    theta1, theta1_vel, theta2, theta2_vel = state

    # Expressions for acceleration
    # 𝜃1
    pendulum1_acc = (m2 * g * np.sin(theta2) * np.cos(theta1 - theta2) - m2 * np.sin(theta1 - theta2) * (
            l1 * theta1_vel ** 2 * np.cos(theta1 - theta2) + l1 * theta2_vel ** 2) -
                     (m1 + m2) * g * np.sin(theta1)) / (l1 * (m1 + m2 * np.sin(theta1 - theta2) ** 2))

    # 𝜃2
    pendulum2_acc = ((m1 + m2) * (
            l1 * theta1_vel ** 2 * np.sin(theta1 - theta2) - g * np.sin(theta2) + g * np.sin(theta1) * np.cos(
        theta1 - theta2)) +
                     m2 * l2 * theta2_vel ** 2 * np.sin(theta1 - theta2) * np.cos(theta1 - theta2)) / (l2 * (
            m1 + m2 * np.sin(theta1 - theta2) ** 2))

    return theta1_vel, pendulum1_acc, theta2_vel, pendulum2_acc

def animate(i,ax,x1,x2,y1,y2):
    x_i = [0, x1[i], x2[i]]
    y_i = [0, y1[i], y2[i]]

    return ax.plot(x_i, y_i, 'o-', color="black")


def double_pendulum():
    theta1 = np.rad2deg(2 * np.pi / 6)
    theta2 = np.rad2deg(5 * np.pi / 8)
    theta1_vel = 0.0
    theta2_vel = 0.0

    state_0 = [theta1, theta1_vel, theta2, theta2_vel]

    l1 = 1.0
    l2 = 1.0
    m1 = 1.0
    m2 = 1.0

    t = np.arange(0, 20, 0.05)
    od = integrate.odeint(get_derivative, state_0, t, args=(l1, l2, m1, m2))

    theta1 = od[:, 0]
    theta2 = od[:, 2]
    # 𝑥1 = 𝑙1𝑠𝑖𝑛 θ1
    x1 = l1 * sin(theta1)
    # 𝑦1 = −𝑙1 cos 𝜃1
    y1 = -l1 * cos(theta1)

    # 𝑥2 = 𝑙1𝑠𝑖𝑛𝜃1 + 𝑙2 sin 𝜃2
    x2 = l1 * sin(theta1) + l2 * sin(theta2)
    # 𝑦2 = −𝑙1 cos 𝜃1 − 𝑙2 cos 𝜃2
    y2 = -l1 * cos(theta1) - l2 * cos(theta2)

    fig = plt.figure()
    ax = fig.add_subplot(111, xlim=(-2, 2), ylim=(-2.5, 2))
    ax.grid()
    ani = animation.FuncAnimation(fig, animate, range(1, len(t)), fargs=(ax,x1,x2,y1,y2),
                                  interval=50, blit=True, )
    plt.show()


double_pendulum()


