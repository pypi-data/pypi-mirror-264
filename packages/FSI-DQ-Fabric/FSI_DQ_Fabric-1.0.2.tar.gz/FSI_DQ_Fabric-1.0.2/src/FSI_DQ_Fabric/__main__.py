import logging

import pandas as pd
import pyspark.pandas as ps
import io
import pyspark.pandas as ps
from FSI_DQ_Fabric.business_contextNB import BusinessContext
#from FSI_DQ.AnomalyDetectionNB import AnomalyDetection
from FSI_DQ_Fabric.Anomaly_multivariateNB import AnomalyDetection
from FSI_DQ_Fabric.StandardizationNB import Standardization

from pyspark.sql import SparkSession


class DataQuality:
    def __init__(self,choice,df,dq_path,partition_field,api_key=None,api_base=None,api_version=None,model_name=None,deployment_name=None,standardization_columns=None,anomalytype=None, column_types=None, columns_and_contamination=None,columns_and_null_handling=None, columns_and_dbscan_params=None,total_contamination=None, total_epsilon=None, min_samples=None):
        
        self.choice=choice
        self.df=df
        self.dq_path=dq_path
        # self.catalog_name=catalog_name
        # self.schema=schema
        self.partition_field=partition_field #""
        

        # self.input_table=input_table


        self.api_key=api_key
        self.api_base=api_base
        self.api_version=api_version
        self.deployment_model=deployment_name
        self.model_name=model_name
        

        self.standardization_columns=standardization_columns

        self.anomalytype=anomalytype
        self.column_types=column_types
        self.columns_and_contamination=columns_and_contamination
        self.columns_and_null_handling=columns_and_null_handling
        self.columns_and_dbscan_params=columns_and_dbscan_params
        self.total_contamination=total_contamination
        self.total_epsilon=total_epsilon
        self.min_samples=min_samples
        
        
    
    def write_delta(df, path, partition, write_mode='overwrite', parts=1):
        """
        Write data into delta lake. If the data is there, overwrite/append it.
        If partitions are specified, partition the data.
    
        :param df(spark dataframe): dataframe to load into deltalake 
        :param path(dict): full path where data will be loaded
        :param partition(list): column names to be partitioned by
        :param parts(string): number of partition files that will be written 
        """
    
        try:

            table_name = path.split("/")[-2]
            
            if partition and partition !="":
                print("partion")
            
                df\
                .coalesce(parts)\
                .write\
                .partitionBy(*list(partition))\
                .format('delta')\
                .mode(write_mode)\
                .option('overwriteSchema', 'true')\
                .option('mergeSchema', 'true')\
                .save(path)
                return "Success"
            else:
            
                df\
                .coalesce(parts)\
                .write\
                .format('delta')\
                .mode(write_mode)\
                .option('overwriteSchema', 'true')\
                .option('mergeSchema', 'true')\
                .save(path)
                
                return "Success"
            
        except Exception as e:
            
            print('error while writing delta', str(e))
            return str(e)




    def main(self):

        try:
            
            spark = SparkSession.builder \
                        .appName("AppName") \
                        .getOrCreate()
            
            # spark.sql(f"USE CATALOG {self.catalog_name}")
            df=self.df
            # df=self.df.toPandas()
            # df=ps.from_pandas(df)
            print('skipping dq rules')

            if self.choice['DQRules']==5:
                bc_df=df.head(10)
                businessContext= BusinessContext(spark,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
                result_bc= businessContext.business_contextFN(bc_df)
                #final_table=f"{self.schema}.BusinessContext" #{self.catalog_name}.
                #result_bc.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                self.write_delta(result_bc, self.dq_path+"/BusinessContext/",self.partition_field)
            
                businessContext= BusinessContext(spark,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
                result_dq= businessContext.dq_rulesFN(df)
                #final_table=f"{self.schema}.DQRules" #{self.catalog_name}.
                #result_dq.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                self.write_delta(result_dq, self.dq_path+"/DQRules/",self.partition_field)

            if self.choice['Standardization']==1:
                df=self.df.toPandas()
                result=Standardization(spark,self.standardization_columns,df,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name).format_issue_detection()
                #final_table=f"{self.schema}.StandardizationResult"#{self.catalog_name}.
                #result.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                print(result)
                print(result.count())
                self.write_delta(result, self.dq_path+"/standardizationResult/",self.partition_field)
                final_table="StandardizationResult"
                result.write.format("delta").mode("overwrite").saveAsTable(final_table)
            print('standardization finished')
            print('started anomaly detection')
            
            if self.choice['AnomalyDetection']==1:
                df_new=df.head(50000)
                # print(len(df_new))
                print('here3',self.columns_and_null_handling)
                result=AnomalyDetection(df_new,self.anomalytype, self.column_types, self.columns_and_null_handling, columns_and_contamination=self.columns_and_contamination, 
                 columns_and_dbscan_params =self.columns_and_dbscan_params, total_contamination=self.total_contamination, total_epsilon=self.total_epsilon, min_samples=self.min_samples).run_anomaly_detection()
                

                result_sp=spark.createDataFrame(result)
                print('detected anomaly , created df')
                path=self.dq_path+"AnomalyDetectionResult/"
                print('here',self.partition_field)
                self.write_delta(result_sp, path,partition=self.partition_field)
                final_table="AnomalyDetectionResult"
                result_sp.write.format("delta").mode("overwrite").saveAsTable(final_table)

            

        except Exception as e:
            raise Exception (e)