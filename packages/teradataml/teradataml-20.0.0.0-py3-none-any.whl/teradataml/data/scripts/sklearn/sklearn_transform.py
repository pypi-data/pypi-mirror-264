import pickle
import math
import os
import sys
import numpy as np

# The below import is needed to convert sparse matrix to dense array as sparse matrices are NOT
# supported in Vantage.
# This is in scipy 1.10.0. Might vary based on scipy version.
from scipy.sparse import csr_matrix

DELIMITER = '\t'

def get_value(value):
    ret_val = value
    try:
        ret_val = float(value.replace(' ', ''))
    except Exception as ex:
        # If the value can't be converted to float, then it is string.
        pass
    return ret_val


def get_values_list(values, ignore_none=True):
    ret_vals = []
    for val in values:
        if val == "" and ignore_none:
            # Empty cell value in the database table.
            continue
        ret_vals.append(get_value(val))

    return ret_vals

def convert_to_type(val, typee):
    if typee == 'int':
        return int(val)
    if typee == 'float':
        return float(val)
    if typee == 'bool':
        return eval(val)
    return str(val)

def splitter(strr, delim=",", convert_to="str"):
    """
    Split the string based on delimiter and convert to the type specified.
    """
    if strr == "None":
        return []
    return [convert_to_type(i, convert_to) for i in strr.split(delim)]

# Process output returned by sklearn function.
def get_output_data(trans_values, func_name, model_obj, n_c_labels):
    # Converting sparse matrix to dense array as sparse matrices are NOT
    # supported in Vantage.
    module_name = model_obj.__module__.split("._")[0]

    if isinstance(trans_values, csr_matrix):
        trans_values = trans_values.toarray()

    if module_name == "sklearn.cross_decomposition" and n_c_labels > 0 and func_name == "transform":
        # For cross_decomposition, output is a tuple of arrays when label columns are provided
        # along with feature columns for transform function. In this case, concatenate the
        # arrays and return the combined values.
        if isinstance(trans_values, tuple):
            return np.concatenate(trans_values, axis=1).tolist()[0]

    if isinstance(trans_values[0], np.ndarray) \
            or isinstance(trans_values[0], list) \
            or isinstance(trans_values[0], tuple):
        # Here, the value returned by sklearn function is list type.
        opt_list = list(trans_values[0])
        if func_name == "inverse_transform" and type(model_obj).__name__ == "MultiLabelBinarizer":
            # output array "trans_values[0]" may not be of same size. It should be of
            # maximum size of `model.classes_`
            # Append None to last elements.
            if len(opt_list) < len(model_obj.classes_):
                opt_list += [""] * (len(model_obj.classes_) - len(opt_list))
        return opt_list
    return [trans_values[0]]

# Arguments to the Script
if len(sys.argv) != 8:
    # 8 arguments command line arguments should be passed to this file.
    # 1: file to be run
    # 2. function name (Eg. predict, fit etc)
    # 3. No of feature columns.
    # 4. No of class labels.
    # 5. Comma separated indices of partition columns.
    # 6. Comma separated types of the partition columns.
    # 7. Model file prefix to generated model file using partition columns.
    # 8. Flag to check the system type. True, means Lake, Enterprise otherwise.
    sys.exit("8 arguments should be passed to this file - file to be run, function name, "\
             "no of feature columns, no of class labels, comma separated indices and types of "\
             "partition columns, model file prefix to generate model file using partition "\
             "columns and flag to check lake or enterprise.")

is_lake_system = eval(sys.argv[7])
if not is_lake_system:
    db = sys.argv[0].split("/")[1]
func_name = sys.argv[1]
n_f_cols = int(sys.argv[2])
n_c_labels = int(sys.argv[3])
data_partition_column_types = splitter(sys.argv[5])
data_partition_column_indices = splitter(sys.argv[4], convert_to="int") # indices are integers.
model_file_prefix = sys.argv[6]

model = None
data_partition_column_values = []

# Data Format:
# feature1, feature2, ..., featuren, label1, label2, ... labelk, data_partition_column1, ..., 
# data_partition_columnn.
# label is optional (it is present when label_exists is not "None")

while 1:
    try:
        line = input()
        if line == '':  # Exit if user provides blank line
            break
        else:
            values = line.split(DELIMITER)
            if not data_partition_column_values:
                # Partition column values is same for all rows. Hence, only read once.
                for i, val in enumerate(data_partition_column_indices):
                    data_partition_column_values.append(
                        convert_to_type(values[val], typee=data_partition_column_types[i])
                        )

                # Prepare the corresponding model file name and extract model.
                partition_join = "_".join([str(x) for x in data_partition_column_values])
                # Replace '-' with '_' as '-' because partition_columns can be negative.
                partition_join = partition_join.replace("-", "_")

                model_file_path = f"{model_file_prefix}_{partition_join}" \
                    if is_lake_system else \
                    f"./{db}/{model_file_prefix}_{partition_join}"

                with open(model_file_path, "rb") as fp:
                    model = pickle.loads(fp.read())

                if not model:
                    sys.exit("Model file is not installed in Vantage.")

            f_ = get_values_list(values[:n_f_cols])
            if n_c_labels > 0:
                # Labels are present in last column.
                l_ = get_values_list(values[n_f_cols:n_f_cols+n_c_labels])
                # predict() now takes 'y' also for it to return the labels from script. Skipping 'y'
                # in function call. Generally, 'y' is passed to return y along with actual output.
                try:
                    # cross_composition functions uses Y for labels.
                    # used 'in' in if constion, as model.__module__ is giving 
                    # 'sklearn.cross_decomposition._pls'.  
                    if "cross_decomposition" in model.__module__:
                        trans_values = getattr(model, func_name)(X=np.array([f_]), Y=np.array([l_]))
                    else:
                        trans_values = getattr(model, func_name)(X=np.array([f_]), y=np.array([l_]))

                except TypeError as ex:
                    # Function which does not accept 'y' like predict_proba() raises error like
                    # "TypeError: predict_proba() takes 2 positional arguments but 3 were given".
                    trans_values = getattr(model, func_name)(np.array([f_]))
            else:
                # If class labels do not exist in data, don't read labels, read just features.
                trans_values = getattr(model, func_name)(np.array([f_]))

            result_list = f_
            if n_c_labels > 0 and func_name in ["predict", "decision_function"]:
                result_list += l_
            result_list += get_output_data(trans_values=trans_values, func_name=func_name,
                                           model_obj=model, n_c_labels=n_c_labels)

            print(*(data_partition_column_values +
                    ['' if (val is None or math.isnan(val) or math.isinf(val))
                     else val for val in result_list]),
                     sep=DELIMITER)

    except EOFError:  # Exit if reached EOF or CTRL-D
        break
