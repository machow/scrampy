from ggplot import *
# Plot segments
def expand_plot(exp):
    exp['TR'] = exp.index
    return ggplot(exp, aes('TR', 'order', color='name')) + geom_point()
