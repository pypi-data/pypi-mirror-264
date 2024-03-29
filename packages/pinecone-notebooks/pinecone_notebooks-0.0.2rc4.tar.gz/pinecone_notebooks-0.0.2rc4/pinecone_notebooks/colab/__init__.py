from IPython.display import HTML, display
from google.colab import output
import os

def SetApiKey(val):
  os.environ['PINECONE_API_KEY'] = val

def Authenticate():
  output.register_callback('pinecone.SetApiKey', SetApiKey)
  display(
    HTML(data='<script type="module">' +
      'import {connectToPinecone} from "https://connect.pinecone.io/embed.js";' +
      'connectToPinecone((val) => google.colab.kernel.invokeFunction("pinecone.SetApiKey", [val], {}), {integrationId: "colab"})' +
      '</script>')
    )
