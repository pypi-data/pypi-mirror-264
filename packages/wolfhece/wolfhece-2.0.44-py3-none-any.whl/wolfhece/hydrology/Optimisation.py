from pathlib import Path
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar,
)

import shutil
import ctypes as ct

from .PostProcessHydrology import PostProcessHydrology
from .Catchment import *
from .Comparison import *
from .read import *
from ..wolf_array import *
from ..PyGui import GenMapManager,HydrologyModel
from . import cst_exchanges as cste
from . import constant as cst
from ..PyTranslate import _


# %% Constants
DLL_FILE = "WolfDll.dll"
DLL_FILE_DEBUG = "WolfDll_debug.dll"



# %% Classes
class CaseOpti(GenMapManager):

    launcherDir:str
    # nbParams:int
    # optiFactor:ct.c_double

    launcherParam:Wolf_Param
    refCatchment:Catchment
    idToolItem:int
    mydro:HydrologyModel

    # FIXME : this variable is just there before the seperation between the object optimisation and GUI optimisation
    wx_exists:bool

    # callBack_proc:dict
    # callBack_ptr:dict

    def __init__(self, *args, **kw):
        self.wx_exists = wx.App.Get() is not None # test if wx App is running
        if self.wx_exists:
            super().__init__(*args, **kw)
        # super().__init__(splash=splash, *args, **kw)

        self.launcherDir = ""
        
    def read_param(self, dir, copyDefault=False, callback=None, workingDir=""):

        self.launcherDir = dir

        if not os.path.exists(self.launcherDir):
            try:
                os.mkdir(self.launcherDir)
                shutil.copyfile(workingDir+"launcher.param.default", os.path.join(self.launcherDir,"launcher.param"))
                shutil.copyfile(workingDir+"launcher.param.default", os.path.join(self.launcherDir,"launcher.param.default"))
            except OSError:
                print ("Creation of the directory %s failed" % self.launcherDir)
            else:
                print ("Successfully created the directory %s" % self.launcherDir)

        if copyDefault:
            shutil.copyfile(workingDir+"launcher.param.default", os.path.join(self.launcherDir,"launcher.param"))
            shutil.copyfile(workingDir+"launcher.param.default", os.path.join(self.launcherDir,"launcher.param.default"))

        self.launcherParam = Wolf_Param(to_read=True, filename=os.path.join(self.launcherDir,"launcher.param"),title="launcher", toShow=False)


    def show_launcherParam(self, event):

        self.launcherParam.Show()
        pass


    def show_mydro(self, event):
        self.mydro.Show()
        pass




class Optimisation(wx.Frame):

    workingDir:str
    # launcherDir:list
    myParams:dict
    myParamsPy:dict
    curParams_vec_F:np.ndarray
    nbParams:int
    optiFactor_F:ct.c_double
    bestFactor:float

    comparHowParam:Wolf_Param
    # launcherParam:Wolf_Param
    saParam:Wolf_Param
    optiParam:Wolf_Param

    # refCatchment:Catchment
    dllFortran:ct.CDLL
    pathDll:str

    callBack_proc:dict
    callBack_ptr:dict

    myCases:list[CaseOpti]

    myStations:list
    compareFilesDict:dict

    # FIXME : this variable is just there before the seperation between the object optimisation and GUI optimisation
    wx_exists:bool

    def __init__(self, parent=None, title="", w=500, h=500, init_wx=True, debugDLL=False):

        self.wx_exists = wx.App.Get() is not None # test if wx App is running

        if self.wx_exists:
            super(Optimisation, self).__init__(parent, title=title, size=(w,h))
        
        self.debugDLL = debugDLL

        self.workingDir = ""
        # self.launcherDir = []
        self.myParams = {}
        self.myParamsPy = {}
        self.nbParams = 0
        self.pathDll = Path(os.path.dirname(__file__)).parent

        self.callBack_proc = {}
        self.callBack_ptr = {}

        self.myCases = []

        self.myStations = []
        self.compareFilesDict = {}

        self.curParams_vec_F = None

        if self.debugDLL:
            self.load_dll(self.pathDll, DLL_FILE_DEBUG)
        else:
            self.load_dll(self.pathDll, DLL_FILE)

        # FIXME
        if self.wx_exists:
            self.initGUI()
    

    def initGUI(self):

        menuBar = wx.MenuBar()

        # Creation of the Menu
        fileMenu = wx.Menu()
        newClick = fileMenu.Append(wx.ID_ANY, 'New')
        self.Bind(wx.EVT_MENU, self.new, newClick)
        openClick = fileMenu.Append(wx.ID_ANY, 'Open')
        self.Bind(wx.EVT_MENU, self.load, openClick)
        resetClick = fileMenu.Append(wx.ID_ANY, 'Reset')
        self.Bind(wx.EVT_MENU, self.reset, resetClick)
        destroyClick = fileMenu.Append(wx.ID_ANY, 'Destroy')
        self.Bind(wx.EVT_MENU, self.destroyOpti, destroyClick)

        fileMenu.AppendSeparator()

        quitClick = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+W')
        fileMenu.Append(quitClick)
        # quitClick = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+W')

        # Creation of the param file Menu
        paramMenu = wx.Menu()
        testOptiClick = paramMenu.Append(wx.ID_ANY, 'test_opti.param')
        self.Bind(wx.EVT_MENU, self.show_optiParam, testOptiClick)
        compareHowClick = paramMenu.Append(wx.ID_ANY, 'compare.how.param')
        self.Bind(wx.EVT_MENU, self.show_comparHowParam, compareHowClick)
        saClick = paramMenu.Append(wx.ID_ANY, 'sa.param')
        self.Bind(wx.EVT_MENU, self.show_saParam, saClick)
        paramMenu.AppendSeparator()
        # add Cases

        # Creation of the Tools Menu
        toolMenu = wx.Menu()
        applyClick = toolMenu.Append(wx.ID_ANY, 'Apply best parameters')
        self.Bind(wx.EVT_MENU, self.apply_optim, applyClick)
        visualiseClick = toolMenu.Append(wx.ID_ANY, 'Visualise best parameters : lumped')
        self.Bind(wx.EVT_MENU, self.plot_optim_sub, visualiseClick)
        visualiseClick_SD = toolMenu.Append(wx.ID_ANY, 'Visualise best parameters : Semi-dist')
        self.Bind(wx.EVT_MENU, self.plot_optim_jct, visualiseClick_SD)
        getRsltClick = toolMenu.Append(wx.ID_ANY, 'Get all outlets')
        self.Bind(wx.EVT_MENU, self.get_all_outlets, getRsltClick)
        getInletsClick = toolMenu.Append(wx.ID_ANY, 'Get all inlets')
        self.Bind(wx.EVT_MENU, self.write_all_inlets, getInletsClick)
        landuseClick = toolMenu.Append(wx.ID_ANY, 'Plot all landuses')
        self.Bind(wx.EVT_MENU, self.plot_all_landuses, landuseClick)
        landuseHydroClick = toolMenu.Append(wx.ID_ANY, 'Plot all hydro landuses')
        self.Bind(wx.EVT_MENU, self.plot_all_landuses_hydro, landuseHydroClick)


        # Creation of the Lauch Menu
        launchMenu = wx.Menu()
        normalLaunchClick = launchMenu.Append(wx.ID_ANY, '1 Basin')
        self.Bind(wx.EVT_MENU, self.launch_lumped_optimisation, normalLaunchClick)
        SDLaunch = launchMenu.Append(wx.ID_ANY, 'Semi-Distributed')
        self.Bind(wx.EVT_MENU, self.launch_semiDistributed_optimisation, SDLaunch)
        SDCompute = launchMenu.Append(wx.ID_ANY, 'Semi-Distributed apply')
        self.Bind(wx.EVT_MENU, self.generate_semiDist_optim_simul, SDCompute)

        # Creation of the Hydro Menu
        hydroSimul = wx.Menu()
        computeHydroClick = hydroSimul.Append(wx.ID_ANY, 'compute')
        self.Bind(wx.EVT_MENU, self.compute0_distributed_hydro_model, computeHydroClick)

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(paramMenu, 'Param files')
        menuBar.Append(toolMenu, 'Tools')
        menuBar.Append(launchMenu, 'Launch')
        menuBar.Append(hydroSimul, 'Hydro')

        # Debug menu
        if(self.debugDLL):
            toolDebug = wx.Menu()
            DebugCompute = toolDebug.Append(wx.ID_ANY, 'Debug all params tests')
            self.Bind(wx.EVT_MENU, self.generate_semiDist_debug_simul, DebugCompute)
            menuBar.Append(toolDebug, 'Debug')

        self.SetMenuBar(menuBar)

        self.SetSize((1700, 900))
        self.SetTitle("Optimisation")
        self.Centre()

        # All Menu bars will be unavailable except the File one
        myExceptions = ['File', 'Hydro']
        self.disable_all_MenuBar(exceptions=myExceptions)

    def quitGUI(self, event):
        self.Close()


    def new(self, event):

        launcherDir = "simul_1"

        # Selection of the working directory
        idir=wx.DirDialog(None,"Choose an optimisation directory")
        if idir.ShowModal() == wx.ID_CANCEL:
            print("Optimisation cancelled!")
            idir.Destroy()

        self.workingDir = idir.GetPath()+"\\"
        launcherDir = os.path.join(self.workingDir,launcherDir)
        idir.Destroy()

        # Launch the Fortran code a first time to generate the default files
        self.default_files(None)

        # Copy and reading of the optiParam file
        shutil.copyfile(self.workingDir+"test_opti.param.default", os.path.join(self.workingDir,"test_opti.param"))
        shutil.copyfile(self.workingDir+"sa.param.default", os.path.join(self.workingDir,"sa.param"))
        shutil.copyfile(self.workingDir+"compare.how.param.default", os.path.join(self.workingDir,"compare.how.param"))
        if not os.path.exists(launcherDir):
            try:
                os.mkdir(launcherDir)
            except OSError:
                print ("Creation of the directory %s failed" % launcherDir)
            else:
                print ("Successfully created the directory %s" % launcherDir)
        shutil.copyfile(self.workingDir+"launcher.param.default", os.path.join(launcherDir,"launcher.param"))
        shutil.copyfile(self.workingDir+"launcher.param.default", os.path.join(launcherDir,"launcher.param.default"))


        # Read the main opti file
        self.optiParam = Wolf_Param(to_read=True, filename=os.path.join(self.workingDir,"test_opti.param"),title="test_opti",toShow=False)
        # # Update all the paths and read all simul
        # self.init_dir_in_params()
        # Read all the param files and init the Case objects and then read the param files associated
        newCase = CaseOpti()
        newCase.read_param(launcherDir, copyDefault=True, callback=self.update_parameters_launcher, workingDir=self.workingDir)
        self.myCases.append(newCase)
        # Update all the paths and read all simul
        self.init_dir_in_params()

        self.comparHowParam = Wolf_Param(to_read=True,filename=os.path.join(self.workingDir,"compare.how.param"),title="compare.how",toShow=False)
        self.saParam = Wolf_Param(to_read=True,filename=os.path.join(self.workingDir,"sa.param"), title="sa",toShow=False)
        self.saParam._callback = self.update_parameters_SA
        # initialise all param files according to the reference characteristics
        self.init_with_reference()
        self.init_myParams()
        self.init_with_default_lumped(replace=True)

        # Case Tool added
        try:
            newId = wx.Window.NewControlId()
            iMenu = self.MenuBar.FindMenu('Param files')
            paramMenu = self.MenuBar.Menus[iMenu][0]
            curName = 'Case '+str(1)
            caseMenu = wx.Menu()
            paramCaseFile = caseMenu.Append(wx.ID_ANY, 'launcher.param')
            self.Bind(wx.EVT_MENU, newCase.show_launcherParam, paramCaseFile)
            guiHydroCase = caseMenu.Append(wx.ID_ANY, 'GUI Hydro')
            curDir = newCase.launcherParam.get_param("Calculs","Répertoire simulation de référence")
            isOk, curDir = check_path(curDir, prefix=self.workingDir, applyCWD=True)
            if isOk<0:
                print("ERROR : in path of launcherDir")
            newCase.mydro = HydrologyModel(dir=curDir)
            newCase.mydro.Hide()
            self.Bind(wx.EVT_MENU, newCase.show_mydro, guiHydroCase)
            curCase = paramMenu.Append(newId, curName, caseMenu)
        except:
            print("ERROR: launch again the app and apply 'load' files.")



        # Let all the menu bars be available in GUI
        self.enable_MenuBar("Param files")
        self.enable_MenuBar("Launch")

    
    def load(self, event, workingDir:str="", fileName:str=""):

        # Selection of the main 
        if workingDir=="":
            idir=wx.FileDialog(None,"Choose an optimatimisation file",wildcard='Fichiers param (*.param)|*.param')
            if idir.ShowModal() == wx.ID_CANCEL:
                print("Post process cancelled!")
                idir.Destroy()
                return
                # sys.exit()
            fileOpti = idir.GetPath()
            readDir = idir.GetDirectory() + "\\"
            idir.Destroy()
        else:
            readDir = workingDir
            if fileName=="": fileName="test_opti.param"
            fileOpti = os.path.join(readDir, fileName)


        # Read the main opti file
        self.optiParam = Wolf_Param(to_read=True, filename=fileOpti, title="test_opti",toShow=False)
        initDir = self.optiParam.get_param("Optimizer","dir")
        isOk, initDir = check_path(initDir, prefix=readDir, applyCWD=True)
        # 
        if os.path.samefile(readDir, initDir):
            self.workingDir = initDir
        else:
            self.workingDir = readDir
            self.optiParam.change_param("Optimizer","dir", self.workingDir)
        nbcases = int(self.optiParam.get_param("Cases","nb"))
        if nbcases>1:
            wx.MessageBox(_('So far, there can only have 1 case! This will change soon.'), _('Error'), wx.OK|wx.ICON_ERROR)
            return
        # self.launcherDir = []
        for i in range(nbcases):
            newCase = CaseOpti()
            launcherDir = self.optiParam.get_param("Cases","dir_"+str(i+1))
            isOk, launcherDir = check_path(launcherDir, prefix=self.workingDir, applyCWD=True)
            if isOk<0:
                print("ERROR : in path of launcherDir")
            newCase.read_param(launcherDir, copyDefault=False, callback=self.update_parameters_launcher)
            # FIXME TO CHANGE when seperation with the GUI
            if self.wx_exists:
                newId = wx.Window.NewControlId()
                iMenu = self.MenuBar.FindMenu('Param files')
                paramMenu = self.MenuBar.Menus[iMenu][0]
                curName = 'Case '+str(i+1)
                iItem = self.MenuBar.FindMenuItem('Param files', curName)
                if(iItem==wx.NOT_FOUND):
                    caseMenu = wx.Menu()
                    paramCaseFile = caseMenu.Append(wx.ID_ANY, 'launcher.param')
                    self.Bind(wx.EVT_MENU, newCase.show_launcherParam, paramCaseFile)
                    guiHydroCase = caseMenu.Append(wx.ID_ANY, 'GUI Hydro')
                    refDir = newCase.launcherParam.get_param("Calculs","Répertoire simulation de référence")
                    isOk, refDir = check_path(refDir, prefix=launcherDir, applyCWD=True)
                    if isOk<0:
                        print("ERROR : in path of launcherDir")
                    newCase.mydro = HydrologyModel(dir=refDir)
                    newCase.mydro.Hide()
                    self.Bind(wx.EVT_MENU, newCase.show_mydro, guiHydroCase)
                    curCase = paramMenu.Append(newId, curName, caseMenu)
                else:
                    print("WARNING : this scenario was not implemented yet. This might induce an error!")
                    # iItem = 
                    curCase = paramMenu.Replace(iItem)
            else:
                refDir = newCase.launcherParam.get_param("Calculs","Répertoire simulation de référence")
                isOk, refDir = check_path(refDir, prefix=launcherDir, applyCWD=True)
                newCase.mydro = HydrologyModel(dir=refDir)
            # self.Bind(wx.EVT_MENU, newCase.show_launcherParam, curCase)
            newCase.idMenuItem = newId
            self.myCases.append(newCase)


        self.comparHowParam = Wolf_Param(to_read=True,filename=os.path.join(self.workingDir,"compare.how.param"),title="compare.how",toShow=False)
        self.saParam = Wolf_Param(to_read=True,filename=os.path.join(self.workingDir,"sa.param"), title="sa",toShow=False)
        for i in range(nbcases):
            self.get_reference(idLauncher=i)
            self.init_myParams(idLauncher=i)

        # Check if the optimisation intervals are within the simulation interval
        self.checkIntervals()

        #
        self.init_with_default_lumped()

        # Let all the menu bars be available in GUI
        self.enable_MenuBar("Param files")
        self.enable_MenuBar("Launch")
        self.enable_MenuBar("Tools")
        if self.debugDLL:
            self.enable_MenuBar("Debug")
    

    def apply_optim(self, event, idLauncher:int=0, replace_only_if_better:bool=False, optim_params:np.ndarray=None):
        """
        Apply optimal parameters based on the results file of the optimisation : ".rpt".

        Args:
            event: The event from the GUI.
            idLauncher (optional: int(0)): The ID of the launcher.
            replace_only_if_better (optional: bool(False) by default): A boolean indicating whether to replace the current parameters if the new ones are better.

        Returns:
            If replace_only_if_better is False, returns the best parameters found.
            If replace_only_if_better is True and the new parameters are better, returns the best parameters found.
            Otherwise, returns None.
        """
        # Get the best parameters
        if optim_params is None:
            bestParams:np.array = self.collect_optim()
        else:
            # FIXME : gneralise the -1 for the test for any number of objective function
            assert self.nbParams==len(optim_params)-1, "ERROR : the number of parameters to appy are the ones expected!"
            bestParams:np.array = optim_params

        test_best = bestParams[-1] # FIXME : gneralise the -1 for the test for any number of objective function
        if not replace_only_if_better:
            self.apply_optim_2_params(bestParams[:-1], idLauncher=idLauncher)
            self.bestFactor = test_best
            return bestParams
        elif test_best>self.bestFactor:
            self.apply_optim_2_params(bestParams[:-1], idLauncher=idLauncher)
            self.bestFactor = bestParams[-1]
            return bestParams
        else:
            return None
        


    # Initialisation of the Optimizer from Fortran
    def init_lumped_hydro(self, event):

        self.init_optimizer()


    
    def init_with_default_lumped(self, replace:bool=False):
        # if replace:
        #     r = wx.ID_NO
        # else:
        #     r = wx.MessageDialog(None, "Do you want to keep your own parameters files?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION).ShowModal()

        # if r != wx.ID_YES:

        #     self.optiParam.change_param("Cases","nb", 1)
        #     self.optiParam.change_param("Optimizer","tuning_method",2)
        #     self.optiParam.change_param("Optimizer","max_nb_run",30000)
        #     self.optiParam.change_param("Comparison factors","nb",1)
        #     self.optiParam.change_param("Comparison factors","which_factor_1",1)

        #     self.comparHowParam.change_param("Comparison global characteristics","nb",1)
        #     self.comparHowParam.change_param("Comparison 1","type",1)
        #     self.comparHowParam.change_param("Comparison 1","nb factors",1)
        #     self.comparHowParam.change_param("Comparison 1","nb intervals",1)
        #     self.comparHowParam.change_param("Comparison 1","factor 1",1)

        #     self.saParam.change_param("Optimisation parameters","eps",1.0E-03)
        #     self.saParam.change_param("Optimisation parameters","rt",0.1)
        #     self.saParam.change_param("Optimisation parameters","ns",10)
        #     self.saParam.change_param("Optimisation parameters","nt",10)
        #     self.saParam.change_param("Optimisation parameters","neps",3)
        #     self.saParam.change_param("Optimisation parameters","Nombre iteration max",500)
        #     self.saParam.change_param("Optimisation parameters","Initial Temperature",20)
        #     self.saParam.callback = self.update_parameters_SA

        #     self.myCases[0].launcherParam.change_param("Calculs","Type de modèle",4)
        #     self.myCases[0].launcherParam.change_param("Calculs","Nombre de simulations parallèles",1)
        #     self.myCases[0].launcherParam.change_param("Récupération des résultats","Nombre de bords de convergence",0)
        #     self.myCases[0].launcherParam.change_param("Récupération des résultats","Nombre de noeuds de convergence",1)
        #     self.myCases[0].launcherParam.change_param("Récupération des résultats","extract_exchange_zone",0)
        #     self.myCases[0].launcherParam.change_param("Récupération des résultats","type_of_geom",2)
        #     self.myCases[0].launcherParam.change_param("Récupération des résultats","type_of_exchange",15)
        #     self.myCases[0].launcherParam.change_param("Récupération des résultats","type_of_data",13)

        #     # if(self.refCatchment.myModel==cst.tom_2layers_linIF):
        #     #     self.init_lumped_model()

        #     self.init_lumped_model()

        #     self.init_myParams()

        #     self.optiParam.SavetoFile(None)
        #     self.optiParam.Reload(None)

        #     self.comparHowParam.SavetoFile(None)
        #     self.comparHowParam.Reload(None)

        #     self.saParam.SavetoFile(None)
        #     self.saParam.Reload(None)

        #     self.myCases[0].launcherParam.SavetoFile(None)
        #     self.myCases[0].launcherParam.Reload(None)
        return


    # def init_2layers_linIF(self):
    def init_lumped_model(self):

        curCase = self.myCases[0]

        self.saParam.change_param("Initial parameters", "Read initial parameters?", 0)

        # Retrieve the dictionnary with the properties of all models (parameters, files, etc)
        myModel = curCase.refCatchment.myModel
        nbParams = cste.modelParamsDict[myModel]["Nb"]
        myModelDict = cste.modelParamsDict[myModel]["Parameters"]

        prefix1 = "param_"
        i=1
        for element in myModelDict:
            paramName = prefix1 + str(i)
            curCase.launcherParam.add_param(groupname=paramName, name="type_of_data", value=element, type="int")
            i+=1

        curCase.launcherParam.change_param("Paramètres à varier","Nombre de paramètres à varier",nbParams)
        self.nbParams = nbParams

        prefix2 = "Parameter "
        for i in range(1,self.nbParams+1):
            paramName = prefix2 + str(i)
            self.saParam.add_param(groupname="Lowest values", name=paramName, value=0.0)
            # if not paramName in self.saParam.myparams["Lowest values"]:
            #     self.saParam.myparams["Lowest values"][paramName] = {}
            #     self.saParam.myparams["Lowest values"][paramName]["value"] = 0.0
            self.saParam.add_param(groupname="Highest values", name=paramName, value=0.0)
            # if not paramName in self.saParam.myparams["Highest values"]:
            #     self.saParam.myparams["Highest values"][paramName] = {}
            #     self.saParam.myparams["Highest values"][paramName]["value"] = 0.0
            if not paramName in self.saParam.myparams["Steps"]:
                self.saParam.myparams["Steps"][paramName] = {}
                self.saParam.myparams["Steps"][paramName]["value"] = 0.0
            self.saParam.add_param(groupname="Initial parameters", name=paramName, value=0.0)
            # if not paramName in self.saParam.myparams["Initial parameters"]:
            #     self.saParam.myparams["Initial parameters"][paramName] = {}
            #     self.saParam.myparams["Initial parameters"][paramName]["value"] = 0.0
            paramName = prefix1 + str(i)
            curCase.launcherParam.add_param(groupname=paramName, name="geom_filename", value="my_geom.txt")
            curCase.launcherParam.add_param(groupname=paramName, name="type_of_geom", value=0)
            curCase.launcherParam.add_param(groupname=paramName, name="type_of_exchange", value=-3)
            # self.myCases[0].launcherParam.myparams[paramName]["geom_filename"] = {}
            # self.myCases[0].launcherParam.myparams[paramName]["geom_filename"]["value"] = "my_geom.txt"
            # self.myCases[0].launcherParam.myparams[paramName]["type_of_geom"] = {}
            # self.myCases[0].launcherParam.myparams[paramName]["type_of_geom"]["value"] = 0
            # self.myCases[0].launcherParam.myparams[paramName]["type_of_exchange"] = {}
            # self.myCases[0].launcherParam.myparams[paramName]["type_of_exchange"]["value"] = -3


    def init_myParams(self, idLauncher=0):
        curCatch:Catchment
        self.nbParams = int(self.myCases[idLauncher].launcherParam.get_param("Paramètres à varier", "Nombre de paramètres à varier"))
        curCatch = self.myCases[idLauncher].refCatchment


        for i in range(1,self.nbParams+1):
            curParam = "param_" + str(i)
            self.myParams[i] = {}
            self.myParams[i]["type"] = int(self.myCases[idLauncher].launcherParam.get_param(curParam, "type_of_data"))
            self.myParams[i]["value"] = 0.0
            # Check cst_echange.py for the values (only consider the param of the Froude model)
            if self.myParams[i]["type"]>100 and self.myParams[i]["type"]<106:
                self.myParams[i]["update"] = curCatch.update_timeDelays_from_F
                self.myParams[i]["junction_name"] = curCatch.junctionOut

            else:
                self.myParams[i]["update"] = self.update_nothing
                self.myParams[i]["junction_name"] = curCatch.junctionOut


            typeParam = int(self.myParams[i]["type"])
            # If it is a Python parameter to optim
            if(typeParam<0):
                self.myParamsPy[i] = self.myParams[i]
                if(typeParam==cste.exchange_parameters_py_timeDelay):
                    self.myParamsPy[i]["update"] = self.myCases[idLauncher].refCatchment.update_timeDelay
                    self.myParamsPy[i]["junction_name"] = self.myCases[idLauncher].launcherParam.get_param(curParam, "junction_name")


    def collect_optim(self, fileName=""):

        isOk,fileName = check_path(fileName, self.workingDir)
        if fileName=="":
            nameTMP = self.optiParam.get_param("Optimizer","fname")
        else:
            isOk,nameTMP = check_path(fileName, self.workingDir)

        optimFileTxt = os.path.join(self.workingDir, nameTMP+".rpt")
        optimFileBin = os.path.join(self.workingDir, nameTMP+".rpt.dat")
        
        isOk, optimFileBin = check_path(optimFileBin)
        if isOk>0:
            optimFile = optimFileBin
            allParams = read_bin(self.workingDir, nameTMP+".rpt.dat", uniform_format=8)
            matrixData = np.array(allParams[-1]).astype("float")
        else:
            isOk, optimFileTxt = check_path(optimFileTxt)
            if isOk>0:
                optimFile = optimFileTxt
                try:
                    with open(optimFile, newline = '') as fileID:
                        data_reader = csv.reader(fileID, delimiter=' ',skipinitialspace=True)
                        list_data = []
                        for raw in data_reader:
                            if(len(raw)>1):
                                if raw[0]+" "+raw[1]=="Best run":
                                    list_data.append(raw[3:-1])
                    matrixData = np.array(list_data[0]).astype("float")
                except:
                    wx.MessageBox(_('The best parameters file is not found!'), _('Error'), wx.OK|wx.ICON_ERROR)

            else:
                logging.error('The best parameters file is not found!')
                return


        return matrixData


    def init_with_reference(self, idLauncher=0):
        
        curCase = self.myCases[idLauncher]
        refCatch = curCase.refCatchment

        # First path opened by the GUI selecting the the working directory
        defaultPath = self.myCases[idLauncher].launcherParam.get_param("Calculs","Répertoire simulation de référence")
        isOk, defaultPath = check_path(defaultPath, self.workingDir)
        if isOk<0:
            defaultPath = ""

        # Selection of the working directory
        idir=wx.FileDialog(None,"Choose a reference file",wildcard='Fichiers post-processing (*.postPro)|*.postPro',defaultDir=defaultPath)
        if idir.ShowModal() == wx.ID_CANCEL:
            print("Post process cancelled!")
            idir.Destroy()

        refFileName = idir.GetPath()
        refDir = idir.GetDirectory() + "\\"
        idir.Destroy()

        myPostPro = PostProcessHydrology(postProFile=refFileName)

        # Recover the Catchment object
        self.myCases[idLauncher].refCatchment = myPostPro.myCatchments["Catchment 1"]['Object']
        curCase.launcherParam.change_param("Calculs", "Répertoire simulation de référence", refCatch.workingDir)

        # Create an empty geom.txt file
        geomName = self.myCases[idLauncher].launcherParam.get_param("Récupération des résultats","geom_filename")
        open(self.myCases[idLauncher].launcherDir[idLauncher]+geomName, mode='a').close()

        # Complete the default model parameters



        # Complete compare.how file
        dateTmp = refCatch.paramsInput.get_param("Temporal Parameters","Start date time")
        self.comparHowParam.change_param("Comparison 1","date begin 1",dateTmp)
        dateTmp = refCatch.paramsInput.get_param("Temporal Parameters","End date time")
        self.comparHowParam.change_param("Comparison 1","date end 1",dateTmp)

        # update param files
        self.myCases[idLauncher].launcherParam.SavetoFile(None)
        self.myCases[idLauncher].launcherParam.Reload(None)
        self.comparHowParam.SavetoFile(None)
        self.comparHowParam.Reload(None)


    def get_reference(self, refFileName="", idLauncher=0):

        if(refFileName==""):
            # First path opened by the GUI selecting the the working directory
            launcherDir = self.optiParam.get_param("Cases","dir_"+str(idLauncher+1))
            isOk, launcherDir = check_path(launcherDir, prefix=self.workingDir, applyCWD=True)
            defaultPath = self.myCases[idLauncher].launcherParam.get_param("Calculs","Répertoire simulation de référence")
            isOk, defaultPath = check_path(defaultPath, launcherDir)
            if isOk<0:
                defaultPath = ""
            idir=wx.FileDialog(None,"Choose a reference file",wildcard='Fichiers post-processing (*.postPro)|*.postPro',defaultDir=defaultPath)
            if idir.ShowModal() == wx.ID_CANCEL:
                print("Post process cancelled!")
                idir.Destroy()
                
            refFileName = idir.GetPath()
            refDir = idir.GetDirectory()
            idir.Destroy()

        myPostPro = PostProcessHydrology(postProFile=refFileName)
        # Recover the Catchment object
        self.myCases[idLauncher].refCatchment = myPostPro.myCatchments["Catchment 1"]['Object']

        # Just save the path in the param file if it is different -> to keep it relative if it is given like that
        if not os.path.samefile(refDir, defaultPath):
            self.myCases[idLauncher].launcherParam.change_param("Calculs", "Répertoire simulation de référence", refDir)

        # Create an empty geom.txt file
        geomName = self.myCases[idLauncher].launcherParam.get_param("Récupération des résultats","geom_filename")
        open(os.path.join(self.myCases[idLauncher].launcherDir,geomName), mode='a').close()

        # update param files
        self.myCases[idLauncher].launcherParam.SavetoFile(None)
        self.myCases[idLauncher].launcherParam.Reload(None)

        # Init the outlet ID
        stationOut = self.optiParam.get_param("Semi-Distributed","Station measures 1")
        if stationOut is None:
            stationOut = self.comparHowParam.get_param("Comparison 1","station measures")
            if stationOut is None:
                stationOut = " "
        else:
            compareFileName = self.optiParam.get_param("Semi-Distributed","File reference 1")
            shutil.copyfile(os.path.join(self.workingDir,compareFileName), os.path.join(self.workingDir,"compare.txt"))
        self.myCases[idLauncher].refCatchment.define_station_out(stationOut)


    def init_dir_in_params(self):

        self.optiParam.change_param("Optimizer","dir", self.workingDir)
        for i in range(len(self.myCases)):
            self.optiParam.change_param("Cases","dir_"+str(i+1), os.path.join(self.workingDir,"simul_"+str(i+1)))
        self.optiParam.change_param("Predefined parameters","fname", os.path.join(self.workingDir,"param.what"))
        self.optiParam.SavetoFile(None)
        self.optiParam.Reload(None)


    def update_dir_in_params(self):

        self.optiParam.change_param("Optimizer","dir", self.workingDir)
        for i in range(len(self.myCases)):
            self.optiParam.change_param("Cases","dir_"+str(i+1), self.myCases[i].launcherDir)
        self.optiParam.change_param("Predefined parameters","fname", os.path.join(self.workingDir,"param.what"))
        self.optiParam.SavetoFile(None)
        self.optiParam.Reload(None)


    def checkIntervals(self):

        print("So far do nothing to check intervals!")
        # self.comparHowParam[]


    def update_parameters_launcher(self, idLauncher=0):
        self.myCases[idLauncher].launcherParam.change_param("Paramètres à varier","Nombre de paramètres à varier",self.nbParams)


    def update_parameters_SA(self):

        # Update the parameters numbers in SA file, according to
        for curGroup in self.saParam.myIncParam:
            for element in self.saParam.myIncParam[curGroup]:
                curParam = self.saParam.myIncParam[curGroup][element]
                if not  "Ref param" in curParam:
                    savedDict = self.saParam.myIncParam[curGroup]["Saved"][curGroup]
                    templateDict = self.saParam.myIncParam[curGroup]["Dict"]
                    for i in range(1,self.nbParams+1):
                        curGroup = curParam.replace("$n$",str(i))
                        if(curGroup in self.saParam.myparams):
                            savedDict[curGroup] = {}
                            savedDict[curGroup] = self.saParam.myparams[curGroup]
                        elif(curGroup in savedDict):
                            self.saParam.myparams[curGroup] = {}
                            self.saParam.myparams[curGroup] = savedDict[curGroup]
                        else:
                            self.saParam.myparams[curGroup] = {}
                            self.saParam.myparams[curGroup] = templateDict.copy()


        # update param files
        # self.launcherParam.SavetoFile(None)
        # self.launcherParam.Reload(None)
        self.saParam.SavetoFile(None)
        self.saParam.Reload(None)


    def plot_optim_sub(self, event, idLauncher=0):
        # this function will plot the hydrographs with the optimal parameters compared to the objective
        figure = Figure(figsize=(5, 4), dpi=100)

        self.axes = figure.add_subplot(111)

        # self.myCases[idLauncher].refCatchment.plot_allSub(withEvap=False, withCt=False, selection_by_iD=self.myCases[idLauncher].refCatchment.myEffSubBasins, \
        #                             graph_title="My optimal configuration", show=True, writeDir=self.workingDir,figure=figure)
        self.myCases[idLauncher].refCatchment.plot_allSub(withEvap=False, withCt=False, selection_by_iD=self.myCases[idLauncher].refCatchment.myEffSubBasins, \
                                    graph_title="My optimal configuration", show=True, writeDir=self.workingDir)

        # self.axes.set_xlabel('x axis')
        self.canvas = FigureCanvas(self, -1, figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)

        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version.
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

        # update the axes menu on the toolbar
        self.toolbar.update()
        self.SetSizer(self.sizer)
        self.Fit()


    def plot_optim_jct(self, event, idLauncher=0):
        # this function will plot the hydrographs with the optimal parameters compared to the objective
        
        refCatch:Catchment = self.myCases[idLauncher].refCatchment

        # Construction of the Measures, in other words the references
        compMeas = []
        if self.myStations==[]:
            self.set_compare_stations(idLauncher=idLauncher)
            
        for iOpti in range(len(self.myStations)):
            dateBegin = refCatch.dateBegin
            dateEnd = refCatch.dateEnd
            deltaT = refCatch.deltaT # [sec]
            stationOut = self.myStations[iOpti]
            compareFileName = self.compareFilesDict[stationOut]
            dir_Meas = self.workingDir
            compMeas.append(SubBasin(dateBegin, dateEnd, deltaT, cst.compare_opti, dir_Meas))
            _,compMeas[iOpti].myHydro = compMeas[iOpti].get_hydro(1, workingDir=dir_Meas, fileNames=compareFileName)

        # Construction of the wx window for plot
        figure = Figure(figsize=(5, 4), dpi=100)

        self.axes = figure.add_subplot(111)

        
        r = wx.MessageDialog(
            None, "Do you want to add a table?", "Plot question",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        ).ShowModal()

        if r == wx.ID_YES:
            addTable = True
        else:
            addTable = False
        # FIXME To remove !!!!
        # ti = datetime.datetime(year=2021, month=7, day=13, hour=0, minute=0, second=0,  microsecond=0, tzinfo=datetime.timezone.utc)
        # tf = datetime.datetime(year=2021, month=7, day=16, hour=6, minute=0, second=0,  microsecond=0, tzinfo=datetime.timezone.utc)
        # rangeData = [ti, tf]
        # refCatch.plot_allJct(Measures=compMeas, withEvap=False, selection_by_key=self.myStations, \
        #                             graph_title="My optimal configurations", show=True, writeDir=self.workingDir, Measure_unit="mm/h", addTable=addTable, rangeData=rangeData)
        refCatch.plot_allJct(Measures=compMeas, withEvap=False, selection_by_key=self.myStations, \
                                    graph_title="My optimal configurations", show=True, writeDir=self.workingDir, Measure_unit="mm/h", addTable=addTable)
        # refCatch.plot_allJct(Measures=compMeas, withEvap=False, selection_by_key=self.myStations, \
        #                             graph_title="My optimal configurations", show=True, writeDir=self.workingDir, Measure_unit="mm/h", addTable=addTable, rangeData=rangeData)

        # refCatch.plot_allJct(Measures=compMeas, withEvap=False, withCt=False, selection_by_key=self.myStations, \
        #                             graph_title="My optimal configurations", show=True, writeDir=self.workingDir,figure=figure)

        # self.axes.set_xlabel('x axis')
        self.canvas = FigureCanvas(self, -1, figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)

        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version.
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

        # update the axes menu on the toolbar
        self.toolbar.update()
        self.SetSizer(self.sizer)
        self.Fit()


    def load_dll(self, path, fileName):
        libpath = os.path.join(path,'libs',fileName)
        try:
            self.dllFortran = ct.CDLL(libpath)
        except:
            print('Erreur de chargement de la librairie WolfDLL.dll')

    def default_files(self, event):

        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = "test_opti.param".encode('ansi')
        self.dllFortran.new_optimizer_files_py.restype = ct.c_int
        self.dllFortran.new_optimizer_files_py.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int]

        print("Launch a Fortran procedure")
        id = self.dllFortran.new_optimizer_files_py(pathPtr,fileNamePtr,ct.c_int(len(pathPtr)),ct.c_int(len(fileNamePtr)))

        print("id optimizer = ", id)

        print("End of Fortran procedure")

    def compute_optimizer(self, idOpti=1):

        self.dllFortran.compute_optimizer_py.restype = ct.c_int
        self.dllFortran.compute_optimizer_py.argtypes = [ct.POINTER(ct.c_int)]

        print("Launch a Fortran procedure")
        isOk = self.dllFortran.compute_optimizer_py(ct.byref(ct.c_int(idOpti)))
        print("End of Fortran procedure")

        if isOk!=0:
            print("ERROR: in the Fotran routine in the optimizer computation!")


    def init_optimizer(self, idForced=-1):

        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = "test_opti.param".encode('ansi')
        self.dllFortran.init_optimizer_py.restype = ct.c_int
        self.dllFortran.init_optimizer_py.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int,ct.POINTER(ct.c_int)]

        if(idForced<0):
            opt_id = None
        else:
            opt_id = ct.byref(ct.c_int(idForced))
        print("Launch a Fortran procedure")
        id = self.dllFortran.init_optimizer_py(pathPtr,fileNamePtr,ct.c_int(len(pathPtr)),ct.c_int(len(fileNamePtr)), opt_id)

        print("id optimizer = ", id)

        print("End of Fortran procedure")


    def init_optimizer_again(self, event, idForced=1):

        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = "test_opti.param".encode('ansi')
        self.dllFortran.init_optimizer_py.restype = ct.c_int
        self.dllFortran.init_optimizer_py.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int,ct.POINTER(ct.c_int)]

        if(idForced<0):
            opt_id = None
        else:
            opt_id = ct.byref(ct.c_int(idForced))
        print("Launch a Fortran procedure")
        id = self.dllFortran.init_optimizer_py(pathPtr,fileNamePtr,ct.c_int(len(pathPtr)),ct.c_int(len(fileNamePtr)), opt_id)

        print("id optimizer = ", id)

        print("End of Fortran procedure")



    def compute_distributed_hydro_model(self, idLauncher=0):

        self.dllFortran.compute_dist_hydro_model_py.restype = ct.c_int
        self.dllFortran.compute_dist_hydro_model_py.argtypes = [ct.c_char_p, ct.c_int]

        pathPtr = self.myCases[idLauncher].refCatchment.workingDir.encode('ansi')

        print("Compute distributed hydro model ...")
        isOk = self.dllFortran.compute_dist_hydro_model_py(pathPtr, ct.c_int(len(pathPtr)))
        print("End of distributed hydro model.")


    def compute0_distributed_hydro_model(self, event):

        self.dllFortran.compute_dist_hydro_model_py.restype = ct.c_int
        self.dllFortran.compute_dist_hydro_model_py.argtypes = [ct.c_char_p, ct.c_int]

        idir=wx.DirDialog(None,"Choose an hydrology directory")
        if idir.ShowModal() == wx.ID_CANCEL:
            print("Hydro computation cancelled!")
            idir.Destroy()
            return
        pathPtr = idir.GetPath().encode('ansi')
        idir.Destroy()


        print("Compute distributed hydro model ...")
        isOk = self.dllFortran.compute_dist_hydro_model_py(pathPtr, ct.c_int(len(pathPtr)))
        print("End of distributed hydro model.")




    def associate_ptr(self, event, which="all", idOpti=1, idLauncher=0):

        self.dllFortran.associate_ptr_py.restype = ct.c_int
        self.dllFortran.associate_ptr_py.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int,
                                                ct.POINTER(ct.c_int), ct.POINTER(ct.c_double)]

        self.dllFortran.get_cptr_py.restype = ct.POINTER(ct.c_double)
        self.dllFortran.get_cptr_py.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int,
                                                ct.POINTER(ct.c_int)]

        self.dllFortran.associate_callback_fct.restype = ct.c_int
        self.dllFortran.associate_callback_fct.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int,
                                                ct.POINTER(ct.c_int), ct.POINTER(ct.c_double)]

        if(which.lower()=="all"):
            self.associate_ptr_params(idOpti,idLauncher)
            self.associate_ptr_opti_factor(idOpti,idLauncher)
            self.associate_ptr_q_all(idOpti,idLauncher)
            if(self.myCases[idLauncher].refCatchment.myModel == cst.tom_2layers_linIF or \
              self.myCases[idLauncher].refCatchment.myModel == cst.tom_2layers_UH):
                self.associate_ptr_time_delays(idOpti,idLauncher)


            self.associate_callback_fct_update(idOpti,idLauncher)
            self.associate_callback_fct_getcvg(idOpti,idLauncher)


    def associate_callback_fct(self):
        print("")


    def associate_callback_fct_update(self, idOpti=1, idLauncher=0):
        # The function proc and ptr should be kept in memory to keep function pointer
        self.callBack_proc[cste.fptr_update] = ct.CFUNCTYPE(ct.c_int, ct.c_int)
        update_proc = self.callBack_proc[cste.fptr_update]
        self.callBack_ptr[cste.fptr_update] = update_proc(self.update_hydro)
        update_ptr = self.callBack_ptr[cste.fptr_update]


        self.dllFortran.associate_callback_fct.restype = ct.c_int
        self.dllFortran.associate_callback_fct.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int,
                                                ct.POINTER(ct.c_int), update_proc]

        # nb of arguments in the dimensions vector (dims)
        ndims = 1
        # init of the dimensions vector
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))

        # Launch Fortran function
        self.dllFortran.associate_callback_fct(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)),
                                            ct.c_int(cste.fptr_update),pointerDims,update_ptr)

        print("End of update pointer association!")



    def associate_callback_fct_getcvg(self, idOpti=1, idLauncher=0):
        self.callBack_proc[cste.fptr_get_cvg] = ct.CFUNCTYPE(ct.c_int, ct.POINTER(ct.c_double))
        getcvg_proc = self.callBack_proc[cste.fptr_get_cvg]
        self.callBack_ptr[cste.fptr_get_cvg] = getcvg_proc(self.get_cvg)
        getcvg_ptr = self.callBack_ptr[cste.fptr_get_cvg]


        self.dllFortran.associate_callback_fct.restype = ct.c_int
        self.dllFortran.associate_callback_fct.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int,
                                                ct.POINTER(ct.c_int), getcvg_proc]

        # nb of arguments in the dimensions vector (dims)
        ndims = 1
        # init of the dimensions vector
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))

        # Launch Fortran function
        self.dllFortran.associate_callback_fct(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)),
                                            ct.c_int(cste.fptr_get_cvg),pointerDims,getcvg_ptr)

        print("End of pointer association!")


    def associate_ptr_q_all(self, idOpti=1, idLauncher=0):
        # nb of arguments in the dimensions vector (dims)
        ndims = 3
        # init of the dimensions vector
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))

        counter = 1
        for iSub in self.myCases[idLauncher].refCatchment.myEffSortSubBasins:
            # curSub = self.refCatchment.subBasinDict[iSub]
            mydict = self.myCases[idLauncher].refCatchment.dictIdConversion
            idIP= list(mydict.keys())[list(mydict.values()).index(iSub)]
            curSub = self.myCases[idLauncher].refCatchment.subBasinDict[idIP]
            dims[2] = counter
            dims[0] = len(self.myCases[idLauncher].refCatchment.time)
            # call of the Fortran function
            curSub.ptr_q_all = None
            curSub.ptr_q_all = self.dllFortran.get_cptr_py(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)),
                                            ct.c_int(cste.ptr_q_all), pointerDims)
            curSub.myHydro = None
            curSub.myHydro = self.make_nd_array(curSub.ptr_q_all, shape=(dims[0],dims[1]), dtype=ct.c_double, order='F', own_data=False)


            # print("output[1,0] = ", curSub.myHydro[1,0])
            # print("output[2,0] = ", curSub.myHydro[2,0])
            # print("output[3,0] = ", curSub.myHydro[3,0])
            # print("output[3,1) = ", curSub.myHydro[3,1])
            # print("curSub = ", curSub.myHydro)
            counter += 1


    def associate_ptr_time_delays(self, idOpti=1, idLauncher=0):
        # nb of arguments in the dimensions vector (dims)
        ndims = 1
        # init of the dimensions vector
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))

        mydict = self.myCases[idLauncher].refCatchment.dictIdConversion
        curCatch:Catchment = self.myCases[idLauncher].refCatchment
        dims[0] = self.myCases[idLauncher].refCatchment.nbSubBasin
        # call of the Fortran function
        curCatch.time_delays_F = None
        curCatch.ptr_time_delays = None
        curCatch.ptr_time_delays = self.dllFortran.get_cptr_py(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)),
                                        ct.c_int(cste.ptr_time_delays), pointerDims)
        curCatch.time_delays_F = self.make_nd_array(curCatch.ptr_time_delays, shape=(dims[0],), dtype=ct.c_double, order='F', own_data=False)



    def associate_ptr_params(self, idOpti=1, idLauncher=0):
        # nb of arguments in the dimensions vector (dims)
        ndims = 1
        # init of the dimensions vector
        dims = np.empty((ndims,), dtype=ct.c_int, order='F')
        # The only dimension is the number of parameters to calibrate
        dims[0] = self.nbParams
        self.curParams_vec_F = np.empty((self.nbParams,), dtype=ct.c_double, order='F')
        # creation of the c_ptr to give to fortran to reconstruct the tensors
        pointerParam = self.curParams_vec_F.ctypes.data_as(ct.POINTER(ct.c_double))
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        # call of the Fortran function
        isOk = self.dllFortran.associate_ptr_py(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)), ct.c_int(cste.ptr_params),
                                        pointerDims, pointerParam)

        print("End of param pointer association.")



    def associate_ptr_opti_factor(self, idOpti=1, idLauncher=0):
        # nb of arguments in the dimensions vector (dims)
        ndims = 1
        # init of the dimensions vector
        dims = np.empty((ndims,), dtype=ct.c_int, order='F')
        # The only dimension is the number of parameters to calibrate
        dims[0] = 1
        self.optiFactor_F = ct.c_double(0.0)
        # creation of the c_ptr to give to fortran to reconstruct the tensors
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        # call of the Fortran function
        isOk = self.dllFortran.associate_ptr_py(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)), ct.c_int(cste.ptr_opti_factors),
                                        pointerDims, ct.byref(self.optiFactor_F))

        print("End of factor pointer association.")


    def init_distributed_hydro_model(self, event):

        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = "test_opti.param".encode('ansi')
        self.dllFortran.init_dist_hydro_model_py.restype = ct.c_int
        self.dllFortran.init_dist_hydro_model_py.argtypes = []

        print("Launch a Fortran procedure")
        id = self.dllFortran.init_dist_hydro_model_py()

        print("id distributed_hydro_model = ", id)

        print("End of Fortran procedure")


    def launch_lumped_optimisation(self, event, idOpti=1):

        # Launch Fortran routine to initialise the object
        self.init_optimizer(idOpti)

        # Associate all the pointers between Python and Fortran
        self.associate_ptr(event, which="all",idOpti=idOpti)

        # Launch Fortran routine to compute optimisation and write the best results
        self.compute_optimizer(idOpti=idOpti)

        print("Best parameters : ", self.curParams_vec_F)
        print("Best Factor = ", self.optiFactor_F)

        # Apply the best parameters
        self.apply_optim(None)

        # Simulation with the best parameters
        self.compute_distributed_hydro_model()

        # Possibility to use the optimisation results enabled
        self.enable_MenuBar("Tools")


    def test_update_hydro_py(self, event):


        self.dllFortran.test_update_hydro.restype = None
        self.dllFortran.test_update_hydro.argtypes = []

        # call of the Fortran function
        self.dllFortran.test_update_hydro()


    def launch_semiDistributed_optimisation(self, event, idOpti=1, idLauncher=0):
        """
        Procedure launching the semi-distributed optimisation process.

        Args:
            event: The event triggering the optimisation.
            idOpti (int): The ID of the optimizer in Fortran.
            idLauncher (int): The ID of the launcher.

        Returns:
            None
        """
        curCatch:Catchment = self.myCases[idLauncher].refCatchment

        if (self.optiParam.get_group("Semi-Distributed"))is not None:
            nbRefs = self.optiParam.get_param("Semi-Distributed","nb")
            onlyOwnSub = self.optiParam.get_param("Semi-Distributed", "Own_SubBasin")
            if onlyOwnSub is None:
                onlyOwnSub = False
            doneList = []
            sortJct = []
            readDict = {}
            previousLevel = 1
            # Read all ref data
            for iRef in range(1, nbRefs+1):
                stationOut = self.optiParam.get_param("Semi-Distributed","Station measures "+str(iRef))
                compareFileName = self.optiParam.get_param("Semi-Distributed","File reference "+str(iRef))
                readDict[stationOut] = compareFileName
            self.compareFilesDict = readDict
            # Get the initial number of intervals 
            # -> these can evolve according to the measurement available at each station
            # FIXME : finish to generalise this part
            nb_comparisons = self.comparHowParam.get_param("Comparison global characteristics","nb")
            nb_intervals_init = [self.comparHowParam.get_param(" ".join(["Comparison",str(i)]),"nb intervals") for i in range(1,nb_comparisons+1)]
            # Get the number of attempts with random initial conditions and from the best parameters for each station
            # The total number of iterations per station is the product of these two numbers :
            # nb_iter total = nb_iter_from_random * nb_iter_from_best
            nb_iter_from_random = self.optiParam.get_param("Optimizer","nb iter from random initial conditions",default_value=1)
            nb_iter_from_best = self.optiParam.get_param("Optimizer","nb iter from best",default_value=1)
            # Check the initial parameters and if they are forced 
            init_params = self.get_initial_parameters()
            # Sort all the junctions by level
            sortJct = curCatch.sort_level_given_junctions(list(readDict.keys()), changeNames=False)
            self.myStations = sortJct

            for iOpti in range(len(sortJct)):
                stationOut = sortJct[iOpti]
                compareFileName = readDict[stationOut]
                # Copy the correct compare.txt file
                shutil.copyfile(os.path.join(self.workingDir,compareFileName), os.path.join(self.workingDir,"compare.txt"))
                # Save the name of the station that will be the output
                curCatch.define_station_out(stationOut)
                # Activate all the useful subs and write it in the param file
                curCatch.activate_usefulSubs(blockJunction=doneList, onlyItself=onlyOwnSub)
                # # Select correct calibration intervals
                # self.select_opti_intervals(stationOut)
                # Rename the result file
                self.optiParam.change_param("Optimizer", "fname", stationOut)
                self.optiParam.SavetoFile(None)
                self.optiParam.Reload(None)
                self.update_myParams(idLauncher)
                # Prepare the paramPy dictionnary before calibration
                self.prepare_calibration_timeDelay(stationOut=stationOut)
                ## loop on the number of different optimisation attempt we would like for each station
                best_params_overall = None
                cur_i = 0
                i_best_overal = 0
                for i_rand in range(nb_iter_from_random):
                    best_params = init_params
                    for i_best in range(nb_iter_from_best):
                        # Prepare I.C. starting from best configuration
                        self.prepare_init_params_from_best(best_params=best_params, idLauncher=idLauncher)
                        # Reload the useful modules
                        self.reload_hydro(idCompar=0, fromStation=stationOut, lastLevel=previousLevel, updateAll=True)
                        # Compute
                        self.init_optimizer(idOpti)
                        self.associate_ptr(None, idOpti=idOpti)
                        self.compute_optimizer(idOpti)
                        # Collect the best parameters and their objective function(s)
                        test_params = self.apply_optim(None, replace_only_if_better=(i_best!=0)) # Always apply the best parameters for the first iteration
                        # If test_params are not the best or 1st test => We don't save them
                        if test_params is not None:
                            best_params = test_params
                            if best_params_overall is None:
                                best_params_overall = best_params
                            elif best_params[-1] > best_params_overall[-1]:
                                best_params_overall = best_params 
                                i_best_overal = cur_i                  
                        # copy the optimisation results to save it on the disk
                        shutil.copyfile(os.path.join(self.workingDir, stationOut+".rpt.dat"), 
                                        os.path.join(self.workingDir, stationOut+"_"+str(cur_i+1)+".rpt.dat"))
                        shutil.copyfile(os.path.join(self.workingDir, stationOut+".rpt"), 
                                        os.path.join(self.workingDir, stationOut+"_"+str(cur_i+1)+".rpt"))
                        cur_i += 1
                # Apply the best parameters overall attemps
                self.apply_optim(None,optim_params=best_params_overall)
                # copy the optimisation results to save it on the disk
                shutil.copyfile(os.path.join(self.workingDir, stationOut+"_"+str(i_best_overal+1)+".rpt.dat"), 
                                os.path.join(self.workingDir, stationOut+".rpt.dat"))
                shutil.copyfile(os.path.join(self.workingDir, stationOut+"_"+str(i_best_overal+1)+".rpt"), 
                                os.path.join(self.workingDir, stationOut+".rpt"))
                
                
                # Simulation with the best parameters
                self.compute_distributed_hydro_model()
                # Update myHydro of all effective subbasins to get the best configuration upstream
                curCatch.read_hydro_eff_subBasin()
                # Update timeDelays according to time wolf_array
                self.apply_timeDelay_dist(idOpti=idOpti, idLauncher=idLauncher, junctionKey=stationOut)
                # Update the outflows
                curCatch.update_hydro(idCompar=0)
                # All upstream elements of a reference will be fixed
                doneList.append(stationOut)
                previousLevel = curCatch.levelOut

        # Possibility to use the optimisation results enabled
        self.enable_MenuBar("Tools")

        print("End of semi-distributed optimisation!")


    # TO DO : Change this function to Case -> to make it compatible with several cases.
    def update_hydro(self, idCompar):

        t0 = time_mod.process_time()
        # Will update all the normal parameters
        for element in self.myParams:
            junctionName = self.myParams[element]["junction_name"]
            paramValue = self.curParams_vec_F[element-1]
            if paramValue != self.myParams[element]["value"]:
                self.myParams[element]["value"] = paramValue
                isOk = self.myParams[element]["update"](junctionName, value=paramValue)


        # # Will update all the Python parameters
        # for element in self.myParamsPy:
        #     junctionName = self.myParamsPy[element]["junction_name"]
        #     timeDelta = self.curParams_vec[element-1]
        #     if timeDelta != self.myParamsPy[element]["value"]:
        #         self.myParamsPy[element]["value"] = timeDelta
        #         # self.myParamsPy[element]["update"](junctionName, value=timeDelta)
        #         isOk = self.myParamsPy[element]["update"](junctionName, value=timeDelta)

        isOk = self.myCases[0].refCatchment.update_hydro(idCompar, fromLevel=False)
        tf = time_mod.process_time()
        print("Time in update_hydro() : ", tf-t0)
        print("curParam = ", self.curParams_vec_F)
        print("All timeDelays = ", self.myCases[0].refCatchment.get_all_timeDelay())
        tf = time_mod.process_time()
        print("Time in update_hydro() : ", tf-t0)
        return isOk
    
    
    def reload_hydro(self, idCompar, firstLevel:int=1, lastLevel:int=-1, fromStation:str="", updateAll:bool=False):

        curCatch:Catchment = self.myCases[0].refCatchment
        isOk = curCatch.construct_hydro(firstLevel=firstLevel, lastLevel=lastLevel,
                                        fromStation=fromStation, updateAll=updateAll)

        return isOk


    # TO DO : Change this function to Case -> to make it compatible with several cases.
    def get_cvg(self, pointerData):

        isOk = self.myCases[0].refCatchment.get_cvg(pointerData)

        return isOk


    def update_timeDelay(self, index):

        isOk = 0.0
        newTimeDelay = self.curParams_vec_F[index-1]
        if(self.myParamsPy[index]["value"]!=newTimeDelay):
            junctionName = self.myParamsPy[index]["junction_name"]
            self.myParamsPy[index]["value"] = newTimeDelay
            isOk = self.myParamsPy[index]["update"](junctionName, value=newTimeDelay)
            # self.refCatchment.reset_timeDelay()
            # isOk = self.refCatchment.update_timeDelay(junctionName, value=newTimeDelay)

        # self.myParamsPy[index]["value"] = newTimeDelay

        return isOk



    def prepare_calibration_timeDelay(self, stationOut, idLauncher=0):

        # Check whether the timeDelay should be calibrated
        readTxt = int(self.optiParam.get_param("Semi-Distributed", "Calibrate_times"))
        if readTxt == 1:
            calibrate_timeDelay=True
        else:
            calibrate_timeDelay=False

        # myModel = self.myCases[idLauncher].refCatchment.myModel
        # nbParamsModel = cste.modelParamsDict[myModel]["Nb"]
        self.remove_py_params(idLauncher)
        nbParamsModel = self.myCases[idLauncher].launcherParam.get_param("Paramètres à varier", "Nombre de paramètres à varier")


        if calibrate_timeDelay:

            # Should delete all the python parameters in both myParams and myParamsPy dictionnaries
            # FIXME To generalise that part
            oldDim = len(self.myParams)
            for i in range(nbParamsModel+1, oldDim+1):
                del self.myParams[i]
                del self.myParamsPy[i]


            inletsNames = self.myCases[idLauncher].refCatchment.get_inletsName(stationOut)
            nbInlets = len(inletsNames)

            nbParams = nbParamsModel + nbInlets
            self.nbParams = nbParams
            self.myCases[idLauncher].launcherParam.change_param("Paramètres à varier", "Nombre de paramètres à varier", nbParams)

            prefix1 = "param_"
            prefix2 = "Parameter "

            for i in range(nbInlets):
                paramName = prefix1 + str(nbParamsModel+i+1)
                # self.myCases[idLauncher].launcherParam.myparams[paramName]={}
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_data"] = {}
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_data"]["value"] = cste.exchange_parameters_py_timeDelay
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_data"]["type"] = 'Integer'
                self.myCases[idLauncher].launcherParam.add_group(paramName)
                self.myCases[idLauncher].launcherParam.add_param(paramName, "type_of_data", cste.exchange_parameters_py_timeDelay, Type_Param.Integer)
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["geom_filename"] = {}
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["geom_filename"]["value"] = "my_geom.txt"
                self.myCases[idLauncher].launcherParam.add_param(paramName, "geom_filename", "my_geom.txt", Type_Param.File)
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_geom"] = {}
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_geom"]["value"] = 0
                self.myCases[idLauncher].launcherParam.add_param(paramName, "type_of_geom", 0, Type_Param.Integer)
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_exchange"] = {}
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["type_of_exchange"]["value"] = -3
                self.myCases[idLauncher].launcherParam.add_param(paramName, "type_of_exchange", -3, Type_Param.Integer)

                # Particularity of this Python parameter
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["junction_name"] = {}
                # self.myCases[idLauncher].launcherParam.myparams[paramName]["junction_name"]["value"] = inletsNames[i]
                self.myCases[idLauncher].launcherParam.add_param(paramName, "junction_name", inletsNames[i], Type_Param.String)

                self.myParams[nbParamsModel+i+1] = {}
                self.myParams[nbParamsModel+i+1]["type"] = self.myCases[idLauncher].launcherParam.get_param(paramName, "type_of_data")
                self.myParams[nbParamsModel+i+1]["value"] = 0.0

                self.myParamsPy[nbParamsModel+i+1] = self.myParams[nbParamsModel+i+1]
                self.myParamsPy[nbParamsModel+i+1]["update"] = self.myCases[idLauncher].refCatchment.update_timeDelay
                self.myParamsPy[nbParamsModel+i+1]["junction_name"] = inletsNames[i]

                # Check and replace the time delay params
                paramName = prefix2 + str(nbParamsModel+i+1)
                cur_param = self.saParam.get_param("Lowest values",paramName)
                if cur_param is None:
                    self.saParam.change_param("Lowest values", paramName, 0.0)
                else:
                    if float(cur_param) != 0.0:
                        logging.warning("The parameters applied to timeDelays are different than the ones recommanded!")
                        logging.warning("This procedure can be dangerous in semi distributed optimisation! Do it at your own risk!")

                cur_param = self.saParam.get_param("Highest values",paramName)
                if cur_param is None:
                    self.saParam.change_param("Highest values", paramName, 5.0*24.0*3600.0)
                else:
                    if float(cur_param) != 5.0*24.0*3600.0:
                        logging.warning("The parameters applied to timeDelays are different than the ones recommanded!")
                        logging.warning("This procedure can be dangerous in semi distributed optimisation! Do it at your own risk!")

                cur_param = self.saParam.get_param("Steps",paramName)
                if cur_param is None:
                    self.saParam.change_param("Steps", paramName, self.myCases[idLauncher].refCatchment.deltaT)
                else:
                    if float(cur_param) != self.myCases[idLauncher].refCatchment.deltaT:
                        logging.warning("The parameters applied to timeDelays are different than the ones recommanded!")
                        logging.warning("This procedure can be dangerous in semi distributed optimisation! Do it at your own risk!")

                cur_param = self.saParam.get_param("Initial parameters",paramName)
                if cur_param is None:
                    self.saParam.change_param("Initial parameters", paramName, 1.0*3600.0)
                else:
                    if float(cur_param) != 1.0*3600.0:
                        logging.warning("The parameters applied to timeDelays are different than the ones recommanded!")
                        logging.warning("This procedure can be dangerous in semi distributed optimisation! Do it at your own risk!")

        else:
            self.nbParams = nbParamsModel
            self.myCases[idLauncher].launcherParam.change_param("Paramètres à varier", "Nombre de paramètres à varier", self.nbParams)


        self.myCases[idLauncher].launcherParam.SavetoFile(None)
        self.myCases[idLauncher].launcherParam.Reload(None)
        self.saParam.SavetoFile(None)
        self.saParam.Reload(None)


    def reset(self, event):

        print("TO DO !!!!")


    def disable_all_MenuBar(self, exceptions=[]):

        for element in range(len(self.MenuBar.Menus)):
            curMenu = self.MenuBar.Menus[element][0]
            nameMenu = self.MenuBar.Menus[element][1]

            if(not(nameMenu in exceptions)):
                self.MenuBar.EnableTop(element, False)


    def enable_MenuBar(self, menuBar:str):

        idMenu = self.MenuBar.FindMenu(menuBar)
        self.MenuBar.EnableTop(idMenu, enable=True)


    def enable_Menu(self, menuItem:str, menuBar:str, isEnable:bool):

        idItem = self.MenuBar.FindMenuItem(menuBar, menuItem)
        objItem = self.MenuBar.FindItemById(idItem)
        objItem.Enable(isEnable)


    def add_Case(self):
        print("TO DO!!!")
        # Add the creation of the case object
        # Add the Case in the ToolBar item


    def launch_optimisation(self, idOpti=1):

        # Check if lumped or semi-distriuted
        if((self.optiParam.get_group("Semi-Distributed"))is not None):
            self.launch_semiDistributed_optimisation(idOpti=idOpti)
        else:
            self.launch_lumped_optimisation(None, idOpti=idOpti)
            self.apply_optim(None)



    def show_optiParam(self, event):

        self.optiParam.Show()
        pass


    def show_saParam(self, event):

        self.saParam.Show()
        pass


    def show_comparHowParam(self, event):

        self.comparHowParam.Show()
        pass


    def update_nothing(self, whatever, value=0.0):

        isOk = 0
        return isOk


    def apply_timeDelay_dist(self, idOpti:int=1, idLauncher:int=0, junctionKey:str=""):

        curRef:Catchment = self.myCases[idLauncher].refCatchment

        if curRef.myModel == cst.tom_2layers_linIF or curRef.myModel == cst.tom_2layers_UH:
            curRef.set_timeDelays(method="wolf_array", junctionKey=junctionKey, updateAll=True)

        # Write all the timeDelays in files
        curRef.save_timeDelays([junctionKey])


    def update_time_delays(self, idOpti:int=1, idLauncher:int=0):
        self.dllFortran.update_time_delay_py.restype = ct.c_int
        self.dllFortran.update_time_delay_py.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
        # call of the Fortran function
        isOk = self.dllFortran.update_time_delay_py(ct.byref(ct.c_int(idOpti)),ct.byref(ct.c_int(idLauncher+1)))

        return isOk

    
    ## Update the dictionnaries of myParams if any changes is identified
    # TODO : Generalised for all type of changes and all the necessary tests -> So far just update the junction name
    def update_myParams(self, idLauncher=0):
        curCatch:Catchment

        curCatch = self.myCases[idLauncher].refCatchment
        for i in range(1,self.nbParams+1):
            curParam = "param_" + str(i)
            self.myParams[i]["junction_name"] = curCatch.junctionOut

    

    ## Function to determine the 
    def set_compare_stations(self, idLauncher):

        if (self.optiParam.get_group("Semi-Distributed"))!=None:
            refCatch = self.myCases[idLauncher].refCatchment
            nbRefs = self.optiParam.get_param("Semi-Distributed","nb")

            readDict = {}
            # Read all ref data
            for iRef in range(1, nbRefs+1):
                stationOut = self.optiParam.get_param("Semi-Distributed","Station measures "+str(iRef))
                compareFileName = self.optiParam.get_param("Semi-Distributed","File reference "+str(iRef))
                readDict[stationOut] = compareFileName
            self.compareFilesDict = readDict
            # Sort all the junctions by level
            self.myStations = refCatch.sort_level_given_junctions(list(readDict.keys()), changeNames=False)


    def destroyOpti(self, event):
        for element in self.myCases:
            element.mydro.Destroy()
            element.Destroy()
        self.Destroy()

        wx.Exit()
        
    
    def get_all_outlets(self, event, idLauncher:int=0):
        # this function will save all the hydrographs with the optimal parameters
        
        refCatch:Catchment = self.myCases[idLauncher].refCatchment
        refCatch.save_ExcelFile_noLagTime()


    def write_all_inlets(self,event, idLauncher:int=0):
        # this function will save the hydrographs and the inlets with the optimal parameters
        refCatch:Catchment = self.myCases[idLauncher].refCatchment
        refCatch.save_ExcelFile_inlets_noLagTime()

    
    def plot_all_landuses(self, event, idLauncher:int=0):
        # this function plots the landuses of all hydro subbasins
        refCatch:Catchment = self.myCases[idLauncher].refCatchment
        refCatch.plot_landuses(onlySub=True, show=True)


    def plot_all_landuses_hydro(self, event, idLauncher:int=0):
        # this function plots the landuses of all hydro subbasins
        refCatch:Catchment = self.myCases[idLauncher].refCatchment
        refCatch.plot_landuses(onlySub=False, show=True)


    ## Apply the best parameters of an optimisation which implies that :
    #   - the ".rpt" file of the results of an optimisation should be present
    #   - the optimal paramters will be replaced in their respective param files
    #   - the timeDelays will then be updated either with :
    #           - Python paramters itself 
    #           - an estimation from the runnof model
    # Once all the optimal parameters are applied, a new simulation is launched to generate the "best" hydrograph
    def generate_semiDist_optim_simul(self, event, idOpti=1,idLauncher:int=0):

        curCatch:Catchment = self.myCases[idLauncher].refCatchment

        if(self.optiParam.get_group("Semi-Distributed"))is not None:
            nbRefs = self.optiParam.get_param("Semi-Distributed","nb")
            onlyOwnSub = self.optiParam.get_param("Semi-Distributed", "Own_SubBasin")
            if onlyOwnSub is None:
                onlyOwnSub = False
            doneList = []
            sortJct = []
            readDict = {}
            # Read all ref data
            for iRef in range(1, nbRefs+1):
                stationOut = self.optiParam.get_param("Semi-Distributed","Station measures "+str(iRef))
                compareFileName = self.optiParam.get_param("Semi-Distributed","File reference "+str(iRef))
                readDict[stationOut] = compareFileName
            self.compareFilesDict = readDict
            # Sort all the junctions by level
            sortJct = curCatch.sort_level_given_junctions(list(readDict.keys()), changeNames=False)
            self.myStations = sortJct

            for iOpti in range(len(sortJct)):
                stationOut = sortJct[iOpti]
                compareFileName = readDict[stationOut]
                # Copy the correct compare.txt file
                shutil.copyfile(os.path.join(self.workingDir,compareFileName), os.path.join(self.workingDir,"compare.txt"))
                # Save the name of the station that will be the output
                curCatch.define_station_out(stationOut)
                # Activate all the useful subs and write it in the param file
                curCatch.activate_usefulSubs(blockJunction=doneList, onlyItself=onlyOwnSub)
                # Rename the result file
                self.optiParam.change_param("Optimizer", "fname", stationOut)
                self.optiParam.SavetoFile(None)
                self.optiParam.Reload(None)
                # 
                self.update_myParams(idLauncher)
                # Preparing the dictionnaries of Parameters to be updated -> not just useful for calibration here !
                self.prepare_calibration_timeDelay(stationOut=stationOut)
                # Fill the param files with their best values
                self.apply_optim(None)
                # Simulation with the best parameters
                self.compute_distributed_hydro_model()
                # Update myHydro of all effective subbasins to get the best configuration upstream
                curCatch.read_hydro_eff_subBasin()
                # Update timeDelays according to time wolf_array
                self.apply_timeDelay_dist(idOpti=idOpti, idLauncher=idLauncher, junctionKey=stationOut)
                # Update the outflows
                curCatch.update_hydro(idCompar=0)
                # All upstream elements of a reference will be fixed
                doneList.append(stationOut)

    
    def generate_semiDist_debug_simul(self, event, idOpti=1,idLauncher:int=0):

        curCatch:Catchment = self.myCases[idLauncher].refCatchment

        if(self.optiParam.get_group("Semi-Distributed"))is not None:
            nbRefs = self.optiParam.get_param("Semi-Distributed","nb")
            onlyOwnSub = self.optiParam.get_param("Semi-Distributed", "Own_SubBasin")
            if onlyOwnSub is None:
                onlyOwnSub = False
            doneList = []
            sortJct = []
            readDict = {}
            # Read all ref data
            for iRef in range(1, nbRefs+1):
                stationOut = self.optiParam.get_param("Semi-Distributed","Station measures "+str(iRef))
                compareFileName = self.optiParam.get_param("Semi-Distributed","File reference "+str(iRef))
                readDict[stationOut] = compareFileName
            self.compareFilesDict = readDict
            # Sort all the junctions by level
            sortJct = curCatch.sort_level_given_junctions(list(readDict.keys()), changeNames=False)
            self.myStations = sortJct

            for iOpti in range(len(sortJct)):
                stationOut = sortJct[iOpti]
                compareFileName = readDict[stationOut]
                # Copy the correct compare.txt file
                shutil.copyfile(os.path.join(self.workingDir,compareFileName), os.path.join(self.workingDir,"compare.txt"))
                # Save the name of the station that will be the output
                curCatch.define_station_out(stationOut)
                # Activate all the useful subs and write it in the param file
                curCatch.activate_usefulSubs(blockJunction=doneList, onlyItself=onlyOwnSub)
                # Rename the result file
                self.optiParam.change_param("Optimizer", "fname", stationOut)
                self.optiParam.SavetoFile(None)
                self.optiParam.Reload(None)
                # 
                self.update_myParams(idLauncher)
                # TO DO -> adapt all the debug_info files
                # write it here !!!!

                # ====
                # Fill the param files and generate all their best configurations
                self.apply_all_tests(idLauncher)
                # Check with a reference
                # TO DO !!!!!

                # All upstream elements of a reference will be fixed
                doneList.append(stationOut)


    def read_all_attempts_SA(self, format="rpt"):
        nameTMP = self.optiParam.get_param("Optimizer","fname")

        if format=="rpt":
            optimFile = os.path.join(self.workingDir, nameTMP+".rpt")

            try:
                with open(optimFile, newline = '') as fileID:
                    data_reader = csv.reader(fileID, delimiter='|',skipinitialspace=True, )
                    list_param = []
                    list_ObjFct = []
                    line = 0
                    for raw in data_reader:
                        if(line<3): 
                            line += 1
                            continue
                        if(len(raw)<=1):
                            break
                        else:
                            usefulData = raw[2:-2]
                            list_param.append(usefulData)
                            list_ObjFct.append(raw[-2])
                        line += 1
                matrixParam = np.array(list_param).astype("float")
                vectorObjFct = np.array(list_ObjFct).astype("float")
            except:
                wx.MessageBox(_('The best parameters file is not found!'), _('Error'), wx.OK|wx.ICON_ERROR)
        
        elif format==".dat":
            optimFile = os.path.join(self.workingDir, nameTMP+".rpt.dat")
            isOk, optimFile = check_path(optimFile)
            if isOk>0:
                allData = read_bin(self.workingDir, nameTMP+".rpt.dat", uniform_format=8)
                allData = np.array(allData).astype("float")
                matrixParam = allData[:-1,:-1]
                vectorObjFct = allData[:-1,-1]

        
        return matrixParam, vectorObjFct
    
    
    def apply_optim_2_params(self, params:np.array, idLauncher=0):

        refCatch:Catchment = self.myCases[idLauncher].refCatchment
        myModel = refCatch.myModel
        filePath = os.path.join(refCatch.workingDir, "Subbasin_" + str(refCatch.myEffSortSubBasins[0]) + "\\")

        myModelDict = cste.modelParamsDict[myModel]["Parameters"]

        if self.curParams_vec_F is None \
           or len(self.curParams_vec_F) != self.nbParams:
            self.curParams_vec_F = np.empty((self.nbParams,), dtype=ct.c_double, order='F')

        for i in range(self.nbParams):
            myType = self.myParams[i+1]["type"]
            if(int(myType)>0):
                self.myParams[i+1]["value"] = params[i]
                fileName = myModelDict[int(myType)]["File"]
                myGroup = myModelDict[int(myType)]["Group"]
                myKey = myModelDict[int(myType)]["Key"]
                if "Convertion Factor" in myModelDict[int(myType)]:
                    convFact = myModelDict[int(myType)]["Convertion Factor"]
                else:
                    convFact = 1.0
                tmpWolf = Wolf_Param(to_read=True, filename=filePath+fileName,toShow=False)
                tmpWolf.myparams[myGroup][myKey]["value"] = params[i]/convFact
                tmpWolf.SavetoFile(None)
                tmpWolf.OnClose(None)
                tmpWolf = None
            else:
                
                self.curParams_vec_F[i] = params[i]
                self.update_timeDelay(i+1)
                refCatch.save_timeDelays([self.myParams[i+1]["junction_name"]])
                print("TO DO : Complete the python parameter dict!!!!!!!")



    def apply_all_tests(self, idLauncher=0):

        refCatch:Catchment = self.myCases[idLauncher].refCatchment

        # Get all the tested parameters
        allParams, objFct = self.read_all_attempts_SA()

        for i in range(len(allParams)):
            curParams = allParams[i]
            self.apply_optim_2_params(curParams, idLauncher=idLauncher)

            # Simulation with the best parameters
            self.compute_distributed_hydro_model()
            # Update myHydro of all effective subbasins to get the best configuration upstream
            refCatch.read_hydro_eff_subBasin()
            # Update the outflows
            refCatch.update_hydro(idCompar=0)



    def remove_py_params(self, idLauncher:int=0):
            """
            Removes the Python parameters from the optimization configuration.

            Args:
                idLauncher (int, optional): The ID of the launcher. Defaults to 0.
            """
            cur_opti = self.myCases[idLauncher]
            paramDict = cur_opti.launcherParam
            nb_params = int(paramDict.get_param("Paramètres à varier", "Nombre de paramètres à varier"))

            myModel = self.myCases[idLauncher].refCatchment.myModel
            nbParamsModel = cste.modelParamsDict[myModel]["Nb"]
            
            for i in range(1,nb_params+1):
                curParam = "param_" + str(i)
                curType = int(paramDict.get_param(curParam, "type_of_data"))
                if curType < 0:
                    del paramDict.myparams[curParam]
                    nb_params -= 1

            # Test
            if nb_params >  nbParamsModel:
                logging.error("The number of to optimise are greater than the number of max parameter of the model!! ")
                return

            self.myCases[idLauncher].launcherParam.change_param("Paramètres à varier", "Nombre de paramètres à varier", nb_params)

            return
    
    
    def select_opti_intervals(self, idLauncher:int=0, stationOut=""):
        cur_opti = self.myCases[idLauncher]
        cur_ref = cur_opti.refCatchment
        if stationOut == "":
            stationOut = cur_ref.junctionOut
        file_compare = os.path.join(self.workingDir,"compare.txt")
        isOk, file_compare = check_path(file_compare)
        if isOk<0:
            logging.error("The file compare.txt is not found!")
            return 
        meas_hydro = SubBasin()

        nb_comparison = self.comparHowParam.get_param("Comparison global characteristics", "nb")
        str_di = "date begin"
        str_df = "date end"
        for icomp in range(1, nb_comparison):
            cur_key = " ".join("Comparison", str(icomp))
            nb_intervals = self.comparHowParam.get_param(cur_key, "nb_intervals")
            for i_inter in range(1,nb_intervals):
                str_read = self.comparHowParam.get_param(" ".join(str_di,str(i_inter)))
                di = datetime.datetime.timestamp(
                    datetime.datetime.strptime(str_read, cst.DATE_FORMAT_HYDRO).replace(tzinfo=datetime.timezone.utc))
                str_read = self.comparHowParam.get_param(" ".join(str_df,str(i_inter)))
                df = datetime.datetime.timestamp(
                    datetime.datetime.strptime(str_read, cst.DATE_FORMAT_HYDRO).replace(tzinfo=datetime.timezone.utc))
                # Check that di is a timestamp lower than other date 


    def prepare_init_params_from_best(self, best_params:np.array, idLauncher:int=0):
        # If there are no best params the initial values will be random
        if best_params is None:
            # Force the initial parameters to be defined randomly
            self.saParam.change_param("Initial parameters", "Read initial parameters?", 0)
            return
        
        # In the following code, we apply the best parameters to the initial parameters
        self.saParam.change_param("Initial parameters", "Read initial parameters?", 1)
        for i in range(self.nbParams):
            self.saParam.change_param("Initial parameters", " ".join(["Parameter",str(i+1)]), best_params[i])
        
        self.saParam.SavetoFile(None)
        self.saParam.Reload(None)

    
    def get_initial_parameters(self)-> np.array:
        read_IP = self.saParam.get_param("Initial parameters", "Read initial parameters?")
        if read_IP == 1:
            # FIXME : Generalise for more than 1 objctive function
            init_params = np.zeros(self.nbParams+1)
            for i in range(self.nbParams):
                init_params[i] = self.saParam.get_param("Initial parameters", " ".join(["Parameter",str(i+1)]))
            init_params[-1] = -sys.float_info.max              
        else:
            init_params = None
        
        return init_params
        
                
    def make_nd_array(self, c_pointer, shape, dtype=np.float64, order='C', own_data=True,readonly=False):
        arr_size = np.prod(shape[:]) * np.dtype(dtype).itemsize

        buf_from_mem = ct.pythonapi.PyMemoryView_FromMemory
        buf_from_mem.restype = ct.py_object
        buf_from_mem.argtypes = (ct.c_void_p, ct.c_int, ct.c_int)
        if readonly:
            buffer = buf_from_mem(c_pointer, arr_size, 0x100)
        else:
            buffer = buf_from_mem(c_pointer, arr_size, 0x200)

        arr = np.ndarray(tuple(shape[:]), dtype, buffer, order=order,)
        if own_data and not arr.flags.owndata:
            return arr.copy()
        else:
            return arr
