import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

class ExploratoryDataAnalysis:
    def __init__(self, data_paths):
        self.data_paths = data_paths
        self.data = None

    def load_data(self, dataset_choice):
        self.data = pd.read_csv(self.data_paths[dataset_choice])

    def run(self):
        st.sidebar.title("Data Exploration and EDA")
        st.sidebar.image("Image/d2.png")

        dataset_choice = st.sidebar.selectbox("Select Dataset", list(self.data_paths.keys()))
        self.load_data(dataset_choice)

        explore_option = st.sidebar.selectbox(
            "Explore Model",
            ["View Data", "View Info", "View Description", "View Missing Values"]
        )

        eda_option = st.sidebar.selectbox(
            "Exploratory Data Analysis",
            ["Select Column", "Univariate Graphs", "Bivariate Graphs", "Multivariate Graphs"]
        )
        st.sidebar.image("Image/d11.png")

        if explore_option == "View Data":
            self.view_data()
        elif explore_option == "View Info":
            self.view_info()
        elif explore_option == "View Description":
            self.view_description()
        elif explore_option == "View Missing Values":
            self.view_missing_values()

        if eda_option == "Univariate Graphs":
            self.univariate_graphs()
        elif eda_option == "Bivariate Graphs":
            self.bivariate_graphs()
        elif eda_option == "Multivariate Graphs":
            self.multivariate_graphs()

    def view_data(self):
        st.title("Data Preview")
        st.image("Image/d6.png")
        st.dataframe(self.data.head())

    def view_info(self):
        buffer = io.StringIO()
        self.data.info(buf=buffer)
        info_str = buffer.getvalue()
        st.write("Data Information")
        st.text(info_str)

    def view_description(self):
        st.write("Data Description")
        st.dataframe(self.data.describe())

    def view_missing_values(self):
        st.write("Missing Values")
        st.dataframe(self.data.isnull().sum())

    def univariate_graphs(self):
        column = st.selectbox("Select Column for Univariate Analysis", self.data.columns)
        plot_type = st.selectbox("Select Plot Type", ["Histogram", "Boxplot", "Countplot"])

        if pd.api.types.is_numeric_dtype(self.data[column]):
            if plot_type == "Histogram":
                fig = px.histogram(self.data, x=column, marginal="box", title="Histogram with Boxplot")
                st.plotly_chart(fig)
            elif plot_type == "Boxplot":
                fig = px.box(self.data, y=column, title="Boxplot")
                st.plotly_chart(fig)
        elif pd.api.types.is_categorical_dtype(self.data[column]) or self.data[column].dtype == 'object':
            if plot_type == "Countplot":
                fig = px.histogram(self.data, y=column, title="Countplot", color=column)
                st.plotly_chart(fig)
        else:
            st.write(f"Cannot plot {plot_type} for column: {column}")

    def bivariate_graphs(self):
        x_column = st.selectbox("Select X-axis Column", self.data.columns)
        y_column = st.selectbox("Select Y-axis Column", self.data.columns)
        plot_type = st.selectbox("Select Plot Type", ["Scatterplot", "Lineplot", "Barplot"])

        if plot_type == "Scatterplot":
            fig = px.scatter(self.data, x=x_column, y=y_column, title="Scatterplot")
            st.plotly_chart(fig)
        elif plot_type == "Lineplot":
            fig = px.line(self.data, x=x_column, y=y_column, title="Lineplot")
            st.plotly_chart(fig)
        elif plot_type == "Barplot":
            fig = px.bar(self.data, x=x_column, y=y_column, title="Barplot", color=x_column)
            st.plotly_chart(fig)

    def multivariate_graphs(self):
        columns = st.multiselect("Select Columns for Multivariate Analysis", self.data.columns)
        plot_type = st.selectbox("Select Plot Type", ["Pairplot", "Heatmap"])

        if plot_type == "Pairplot":
            if all(pd.api.types.is_numeric_dtype(self.data[col]) for col in columns):
                fig = px.scatter_matrix(self.data, dimensions=columns, title="Pairplot")
                st.plotly_chart(fig)
            else:
                st.write("All selected columns must be numeric for Pairplot.")
        elif plot_type == "Heatmap":
            if len(columns) > 1 and all(pd.api.types.is_numeric_dtype(self.data[col]) for col in columns):
                corr_matrix = self.data[columns].corr()
                fig = go.Figure(
                    data=go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale="coolwarm",
                        colorbar=dict(title="Correlation"),
                    )
                )
                fig.update_layout(title="Heatmap")
                st.plotly_chart(fig)
            else:
                st.write("Select at least two numeric columns for a Heatmap.")

# Uncomment the following lines to run the app
# if __name__ == "__main__":
#     data_paths = {
#         "Dataset 1": "path_to_dataset1.csv",
#         "Dataset 2": "path_to_dataset2.csv"
#     }
#     eda = ExploratoryDataAnalysis(data_paths)
#     eda.run()
