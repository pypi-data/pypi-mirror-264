import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


class AnomalyDetection:
    def __init__(self, df, anomalytype, column_types, columns_and_null_handling, columns_and_contamination=None, 
                 columns_and_dbscan_params=None, total_contamination=None, total_epsilon=None, min_samples=None):
        # self.inputfile = inputfile
        # self.outputfile = outputfile

        self.df=df
        self.anomalytype = anomalytype
        self.column_types = column_types
        self.columns_and_contamination = columns_and_contamination
        self.columns_and_null_handling = columns_and_null_handling
        self.columns_and_dbscan_params = columns_and_dbscan_params
        self.total_contamination = total_contamination
        self.total_epsilon = total_epsilon 
        self.min_samples = min_samples

    # def load_dataset(self):
    #     try:
    #         dataset = pd.read_csv(self.inputfile)
    #         return dataset
    #     except Exception as e:
    #         print(f"Error loading dataset: {str(e)}")
    #         return None

    def select_columns(self, dataset, columns_to_use):
        print(columns_to_use)
        selected_data = dataset[columns_to_use]
        return selected_data

    def replace_null_with_mean(self, data):
        return data.fillna(data.mean())

    def replace_null_with_zero(self, data):
        return data.fillna(0)

    def apply_scaling(self, data):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)

    def apply_isolation_forest(self, data, contamination):
        data_copy = data.copy()
        isolation_forest = IsolationForest(contamination=contamination)
        data_copy['IFanomaly'] = isolation_forest.fit_predict(data)
        data_copy['IF_decision_score_'] = isolation_forest.decision_function(data)
        return data_copy

    def apply_dbscan(self, data, eps, min_samples):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        data['DBSCAN_Labels'] = dbscan.fit_predict(data)
        return data

    def preprocess_data(self, data, target_column):
        label_encoder = LabelEncoder()
        data[target_column] = label_encoder.fit_transform(data[target_column])
        return data

    def run_anomaly_detection(self):
        dataset = self.df
        output_data = dataset.copy()
        processed_data = pd.DataFrame()

        if self.anomalytype == 'univariate':
            for column, column_type in self.column_types.items():
                if column_type == 'numeric':
                    contamination_factor = self.columns_and_contamination.get(column)
                    selected_data = self.select_columns(dataset, [column])
                    null_handling_method = self.columns_and_null_handling.get(column)#'mean')

                    if null_handling_method == 'mean':
                        selected_data = self.replace_null_with_mean(selected_data)
                    elif null_handling_method == 'zero':
                        selected_data = self.replace_null_with_zero(selected_data)
                    else:
                        print(f"Invalid null handling method for column '{column}'. Using 'mean' as default.")
                        selected_data = self.replace_null_with_mean(selected_data)

                    scaled_data = self.apply_scaling(selected_data)
                    data_with_if_anomaly = self.apply_isolation_forest(scaled_data, contamination_factor)
                    dbscan_params = self.columns_and_dbscan_params.get(column)
                    data_with_dbscan = self.apply_dbscan(scaled_data, eps=dbscan_params['eps'], min_samples=dbscan_params['min_samples'])

                    output_data[f'{column}_IFanomaly'] = data_with_if_anomaly['IFanomaly']
                    output_data[f'{column}_DBSCAN_Labels'] = data_with_dbscan['DBSCAN_Labels']

                elif column_type == 'non-numeric':
                    print(f"Processing non-numeric column '{column}'")
                    selected_data = self.select_columns(output_data, [column])
                    selected_data = self.preprocess_data(selected_data, column)
                    dbscan_params = self.columns_and_dbscan_params.get(column)
                    data_with_dbscan = self.apply_dbscan(selected_data, eps=dbscan_params['eps'], min_samples=dbscan_params['min_samples'])
                    output_data[f'{column}_DBSCAN_Labels'] = data_with_dbscan['DBSCAN_Labels']

        elif self.anomalytype == 'multivariate':
            for column, column_type in self.column_types.items():
                if column_type == 'numeric':
                    print(f"Processing numeric column '{column}'")
                    selected_data = self.select_columns(dataset, [column])
                    null_handling_method = self.columns_and_null_handling.get(column)

                    if null_handling_method == 'mean':
                        selected_data = self.replace_null_with_mean(selected_data)
                    elif null_handling_method == 'zero':
                        selected_data = self.replace_null_with_zero(selected_data)
                    else:
                        print(f"Invalid null handling method for column '{column}'. Using 'mean' as default.")
                        selected_data = self.replace_null_with_mean(selected_data)

                    scaled_data = self.apply_scaling(selected_data)
                    processed_data[f'{column}_scaled'] = scaled_data

                elif column_type == 'non-numeric':
                    print(f"Processing non-numeric column '{column}'")
                    selected_data = self.select_columns(output_data, [column])
                    selected_data = self.preprocess_data(selected_data, column)
                    processed_data[f'{column}_label_encode'] = selected_data
            print('conti,',self.total_contamination)
            data_with_if_anomaly = self.apply_isolation_forest(processed_data, self.total_contamination)
            data_with_dbscan = self.apply_dbscan(processed_data, eps=self.total_epsilon, min_samples=self.min_samples)
            output_data['IFanomaly'] = data_with_if_anomaly['IFanomaly']
            output_data['IF_decision_score_'] = data_with_if_anomaly['IF_decision_score_']
            output_data['DBSCAN_Labels'] = data_with_dbscan['DBSCAN_Labels']
            # self.plot_anomaly(processed_data, output_data['IF_decision_score_'])
            # self.plot_prediction(processed_data, output_data['IFanomaly'])
            # print('************************Isolation Forest************************')
            # self.precision_and_recall(output_data['Manual_Label'],output_data['IFanomaly'])
            # print('************************Isolation Forest Decision Score************************')
            # self.precision_and_recall(output_data['Manual_Label'],output_data['IF_decision_score_'])
            # print('************************DBSCAN************************')
            # self.precision_and_recall(output_data['Manual_Label'],output_data['DBSCAN_Labels'])
        return output_data

    ######### Visualize Anomaly scores and Anomaly Status ########
    def plot_anomaly(self, data, anomaly_score):
        if data.shape[1]==2:
            plt.figure(figsize = (10, 6), dpi = 150)
            # s = plt.scatter(data[f'{self.target_columns[0]}'], data[f'{self.target_columns[1]}'], c = anomaly_score, cmap = 'coolwarm')
            s = plt.scatter(data.iloc[:,0], data.iloc[:,1], c = anomaly_score, cmap = 'coolwarm')
            plt.colorbar(s, label = 'More Negative = More Anomalous')
            plt.xlabel(f'{self.target_columns[0]}', fontsize = 16)
            plt.ylabel(f'{self.target_columns[1]}', fontsize = 16)
            plt.grid()
            plt.title(f'Anomaly Score', weight = 'bold')
        elif data.shape[1]>=3:
            self.PCA_plot(2, data)

    
    # To Plot Predictions    
    def plot_prediction(self, data, predictions):
        if data.shape[1]==2:
            plt.figure(figsize = (10, 6), dpi = 150)
            # s = plt.scatter(data[f'{self.target_columns[0]}'], data[f'{self.target_columns[1]}'], c = predictions, cmap = 'coolwarm')
            s = plt.scatter(data.iloc[:,0], data.iloc[:,1], c = predictions, cmap = 'coolwarm')
            plt.colorbar(s, label = 'More Negative = More Anomalous')
            plt.xlabel(f'{self.target_columns[0]}', fontsize = 16)
            plt.ylabel(f'{self.target_columns[1]}', fontsize = 16)
            plt.grid()
            plt.title(f'Contamination = {self.total_contamination}', weight = 'bold')
        elif data.shape[1]>=3:
            self.PCA_plot(2, data)

    #PCA
    def PCA_plot(self, dimension, data):
        target_column = ["Price_scaled", "StockLevel_scaled","Item Category_label_encode"]
        pca = PCA(dimension)
        pca.fit(data)
        res = pd.DataFrame(pca.transform(data))
        # res.head(10)
        # Z = np.array(res)
        # plt.title("IsolationForest")

        plt.figure(figsize = (10, 6), dpi = 150)
        s = plt.scatter(res[0], res[1], c = data.IF_decision_score_, cmap = 'coolwarm')
        plt.colorbar(s, label = 'More Negative = More Anomalous')
        plt.xlabel(f'res_1', fontsize = 16)
        plt.ylabel(f'res_2', fontsize = 16)
        plt.grid()
        plt.title(f'Contamination = {self.total_contamination}', weight = 'bold')



    def precision_and_recall(self, y, y_pred):
        # Calculate the number of True Positives (correctly predicted anomalies)
        true_positives = sum(1 for true_label, predicted_label in zip(y, y_pred) if true_label == -1 and predicted_label == -1)

        # Calculate the number of False Negatives (anomalies not detected by the model)
        false_negatives = sum(1 for true_label, predicted_label in zip(y, y_pred) if true_label == -1 and predicted_label == 1)

        # Calculate the number of False Positives
        false_positives = sum(1 for true_label, predicted_label in zip(y, y_pred) if true_label == 1 and predicted_label == -1)
        
        # Calculate the total number of anomalies in the dataset
        total_anomalies = sum(1 for label in y if label == -1)
        
        # Calculate the ratio of correctly predicted anomalies to total anomalies
        recall = true_positives / total_anomalies
        if (true_positives + false_positives) == 0:
            precision = 0
        else:
            precision  = true_positives/ ( true_positives + false_positives)
        print(f'Precision:{precision}')
        print(f'Recall:{recall}')

# # Parameters
# inputfile = 'Financial_Sample1.csv'
# outputfile = 'Financial_Sample_output2.csv'
# anomalytype =  "multivariate" #"univariate"

# # column_types = {'Units Sold': 'numeric','Product': 'non-numeric'}
# # target_columns  = ['Units Sold', 'Product']
# # columns_and_contamination = {'Units Sold': 0.1,'Product':'zero'}
# # columns_and_null_handling = {'Units Sold': 'mean'}
# # columns_and_dbscan_params = {'Units Sold': {'eps': 0.5, 'min_samples': 5}, 'Product': {'eps': 0.3, 'min_samples': 10},
# #                              }

# # column_types = {'Salary': 'numeric', 'Designation': 'non-numeric'}
# # columns_and_contamination = {'Salary': 0.1, 'Designation': 0.1}
# # columns_and_null_handling = {'Salary': 'mean'}
# # columns_and_dbscan_params = {'Designation': {'eps': 0.5, 'min_samples': 7}, 'Salary': {'eps': 0.3, 'min_samples': 10}}

# column_types = {'Prod': 'non-numeric','Manu_price': 'numeric'}
# columns_and_contamination = {'Prod': 0.1, 'Manufacturing_Price': 0.1}
# columns_and_null_handling = {'Manu_price': 'mean'}
# columns_and_dbscan_params = {'Prod': {'eps': 0.5, 'min_samples': 5}, 'Manu_price': {'eps': 0.5, 'min_samples': 5}}

# total_contamination = 0.1
# total_epsilon = 0.1
# min_samples = 100

# # Create an instance of the AnomalyDetection class and run the anomaly detection
# anomaly_detection = AnomalyDetection(inputfile, outputfile, anomalytype, column_types, columns_and_contamination,
#                                      columns_and_null_handling, columns_and_dbscan_params, total_contamination, total_epsilon, min_samples)

# anomaly_detection.run_anomaly_detection()