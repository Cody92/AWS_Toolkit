import requests
import boto3

lambda_client = boto3.client('lambda')

def download_lambda():
   nextMarker = ''
   lambdafunctionArnList = []
   while nextMarker != None:
       if nextMarker == '':
           response = lambda_client.list_functions(
           MaxItems=50
           )
       else:
           response = lambda_client.list_functions(
           Marker=nextMarker,
           MaxItems=50
           ) 
       for func in response.get('Functions'):
           lambdafunctionArnList.append(func.get('FunctionArn'))
       nextMarker = response.get('NextMarker')
   
   print(f'Total lambda functions: {len(lambdafunctionArnList)}') 

   tmp_dir = 'download_all_lambda/' 

   for function_arn in lambdafunctionArnList:
       arn = function_arn
       arn_parts = arn.split(':')
       func_name = arn_parts[6]
   
       func_details = lambda_client.get_function(FunctionName=function_arn)
       zip_file = tmp_dir + func_name + '.zip'
       url = func_details['Code']['Location']
   
       r = requests.get(url)
       with open(zip_file, "wb") as code:
           code.write(r.content)
   
   print("Download complete!")

download_lambda()