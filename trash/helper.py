import matplotlib.pyplot as plt

# from IPython import display

# plt.ion()


def plot(scores, n):
    # display.clear_output(wait=True)
    # display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Number of Games")
    plt.ylabel("Won Rate")
    plt.plot(scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.savefig("./result/result_n_{}.png".format(n))
    # plt.show(block=False)
    # plt.pause(0.1)
