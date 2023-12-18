# Scrpts to run transformation of the parquet file of chess 
# With multicore by multiprocessing and mutlinode by mpi4py
# Example:
# run with 4 nodes, mpirun -np 4 python transform.py 

input_folder = r'your_folder_path' # Folder contain raw parquet files.
output_folder = r'your_folder_path' # Folder save the transformed parquet files.

import os
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
from utils import transform_example
from mpi4py import MPI
import pandas as pd

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

files = os.listdir(input_folder)
files_per_process = len(files) // size
start_index = rank * files_per_process
end_index = start_index + files_per_process if rank != size - 1 else len(files)

for i in range(start_index, end_index):
    file_path = os.path.join(input_folder, files[i])
    out_path = os.path.join(output_folder, files[i])

    if os.path.isfile(out_path):
        continue
    
    try:
        print(f"{file_path} from {rank}")        
        df = pd.read_parquet(file_path)
        num_cores = cpu_count() 
        chunks = np.array_split(df, num_cores)  # Split DataFrame into chunks

        def process_chunk(chunk):
            return chunk.apply(transform_example, axis=1)
        with Pool(num_cores) as p:
            results = p.map(process_chunk, chunks)

        new_df = pd.concat(results).to_frame()
        new_df.to_parquet(out_path)
        # TODO shall we support multi format like json here?

    except Exception as e:
        print(f"error {e} occur from {rank} when processing {file_path}")
