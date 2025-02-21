# init conda shell
conda init --all

# create arcgis environment
conda create -n arcgis -c esri arcgis arcgis-mapping --yes --quiet

# set default environment on terminal load
echo "conda activate arcgis" >> ~/.bashrc
echo "conda activate arcgis" >> ~/.zshrc
