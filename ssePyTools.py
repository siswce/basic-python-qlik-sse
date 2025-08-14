"""
@author:        Wilson Chavez
@create:        2025-07-30
@description:   basic example of a server-side extension (SSE) for Qlik Sense
@version:       1.0
@license:       MIT
"""

import grpc
import logging
import time
import platform
import multiprocessing
from concurrent import futures

import ServerSideExtension_pb2 as SSE
import ServerSideExtension_pb2_grpc as SSE_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if platform.system() == "Windows":
    try:
        multiprocessing.set_start_method('spawn')
    except RuntimeError:
        pass
        
class ExtensionService(SSE_grpc.ConnectorServicer):
    def __init__(self):
        self.function_definitions = {
            0: {
                'name': 'calcBmi',
                'function_type': SSE.SCALAR,
                'return_type': SSE.NUMERIC,
                'params': [SSE.NUMERIC, SSE.NUMERIC]
            }
        }
    
    def GetCapabilities(self, request, context):
        try:       
            capability = SSE.Capabilities()
            capability.allowScript = False
            capability.pluginIdentifier = "Calculate BMI"
            capability.pluginVersion = "1.0"
            
            # Add functions
            for func_id, func_def in self.function_definitions.items():
                function = capability.functions.add()
                function.name = func_def['name']
                function.functionId = func_id
                function.functionType = func_def['function_type']
                function.returnType = func_def['return_type']
                
                # Add parameters
                for param_type in func_def['params']:
                    parameter = function.params.add()
                    parameter.dataType = param_type
                    
        except Exception as e:
            logger.error(f"Error {type(e)} in GetCapabilities: {e}")
            
        logger.info("Capabilities sent to QlikSense")
        return capability  
        
    def ExecuteFunction(self, request_iterator, context):
        try:  
            # Process each row of data
            for request_rows in request_iterator:
                # Handle different request formats
                if hasattr(request_rows, 'rows'):
                    rows_to_process = request_rows.rows
                else:
                    # If request_rows is the actual row data
                    rows_to_process = [request_rows] if hasattr(request_rows, 'duals') else []
            
                for row in rows_to_process:
                    result = self.calculate_bmi(row)
                    # Create response
                    response = SSE.BundledRows()
                    response.rows.append(result)
                    yield response
                    
        except Exception as e:
            logger.error(f"Error {type(e)} in ExecuteFunction: {e}")
            
            yield SSE.BundledRows(rows=[
                SSE.Row(duals=[SSE.Dual(numData=0, strData=f"Error: {str(e)}")])
            ])
                
    def calculate_bmi(self, row):
        try:
            # Extract weight and height from the row
            weight= row.duals[0].numData
            height= row.duals[1].numData    
            
            bmi=float('nan')
            if height>0:
                bmi= weight / (height ** 2)
            
            # Create result row
            result_row = SSE.Row(duals=[SSE.Dual(numData=round(bmi, 2), strData=f"result")])
            return result_row
            
        except Exception as e:
            logger.error(f"Error {type(e)} in calculate_bmi: {e}")
            result_row = SSE.Row(duals=[SSE.Dual(numData=0, strData=f"Error: {str(e)}")])
            return result_row
        
def main():
    num_cpus = multiprocessing.cpu_count()
    num_workers = max(1, min(num_cpus - 1, 8))
    
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=num_workers))
    SSE_grpc.add_ConnectorServicer_to_server(ExtensionService(), server)
    
    # Listen on port 50051
    port = '50051'
    server.add_insecure_port(f'[::]:{port}')
    
    # Start server
    server.start()
    logger.info(f"Server SSE running on port {port}")
    
    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        logger.info("Stopping server...")
        server.stop(0)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()