import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Define confusion matrices for 7 metrics, each with 3 confusion matrices
metrics_data = {
    f"Metric_{i+1}": [np.random.randint(0, 100, size=(2, 2)) for _ in range(3)] for i in range(7)
}

def to_pdf(metrics_data, filename):
    n_rules = len(metrics_data[list(metrics_data.keys())[0]])

    #n_rules = n_rules if n_rules < 5 else 5
    #x = int(sqrt(len(self.rules))) if int(sqrt(len(self.rules))) < 10 else 10

    ratios = [1 if i == 0 else 7 for i in range(n_rules//5+1)]

    coord = [(i//5+1,i%5) for i in range(n_rules)]

    # Define figure size for each confusion matrix
    figsize = (n_rules*5 if n_rules<5 else 25, (n_rules//5)*5+1 if n_rules>5 else 6)
    pdf_pages = PdfPages(f'{filename}.pdf')

    for metric, confusion_matrices in metrics_data.items():
        fig = plt.figure(figsize=figsize)

        # Create a gridspec to accommodate an additional "title" axis
        gs = fig.add_gridspec(n_rules//5+1, n_rules if n_rules<5 else 5, hspace=0.4,height_ratios=ratios)

        # Create "title" axis and add title
        title_ax = fig.add_subplot(gs[0, :])
        title_ax.text(0.5, 0.5, metric.capitalize(), ha="center", va="center", fontsize=14)
        title_ax.axis("off")
        #print(coord)

        for i, conf_matrix in enumerate(confusion_matrices):
            #ax = fig.add_subplot(gs[1, i])
            #print(coord[i])
            ax = fig.add_subplot(gs[coord[i]])

            # Heatmap plot with seaborn
            sns.heatmap(conf_matrix, annot=True, fmt="d", cmap='Blues',cbar=False, ax=ax)
            ax.set_title(f'Confusion Matrix: Rule {i+1}')
            ax.set_xlabel('Real label')
            ax.set_ylabel('Predicted label')
            ax.set_xticklabels(['True', 'False'])
            ax.set_yticklabels(['True', 'False'])


        # Ensure the plot is displayed properly with xticks and yticks
        #plt.tight_layout()

        # Save the figure to the pdf file
        pdf_pages.savefig(fig)
        plt.close()
    # Close the pdf file
    pdf_pages.close()