import os

"""
Arcana Engine
Asset load manager
In an effort to regulate asset loading for the game, this script will automatically find and load assets from the asset folder
Reads through the asset folder and stores paths to asset collections in a dict which is returned
"""

class assetLoader:
    def __init__(self):
        self.assetBundles = {}
        assetFolder = "Arcana-Engine\Assets"
        assetGroupNames = os.listdir(assetFolder)
        for assetBundle in assetGroupNames:
            self.assetBundles[assetBundle] = os.path.join(assetFolder, assetBundle)
            print(self.assetBundles[assetBundle])

    def getAssetBundles(self):
        return self.assetBundles
    
if __name__ == "__main__":
    testLoader = assetLoader()

        