#pyGHDL libraries
import pyGHDL.libghdl     as libghdl
from pyGHDL.libghdl       import name_table, files_map, errorout_console
from pyGHDL.libghdl.vhdl  import nodes, sem_lib
import pyGHDL.libghdl.utils as pyutils
import pyGHDL.libghdl.vhdl.nodes_meta as nodes_meta
import sys

#xml parsing
from xml.dom import minidom


class RCpyGHDL:
    handbook="handbook_STD_CNE_17062021.xml"

    def __init__(self, ghdl_option,filename):
        """Initialization: set Ghdl options for filename analysis 
                           get parameters from handbook """  

        self.ghdl_option=str(ghdl_option)
        self.filename=str(filename)

        
        libghdl.initialize()

        # Print error messages on the console.
        errorout_console.Install_Handler()
        
        # Set options. This must be done before analyze_init()
        libghdl.set_option(self.ghdl_option)

        # Finish initialization. This will load the standard package.
        try:
            if libghdl.analyze_init_status() != 0:
                print("ERROR libghdl initialization")
                quit()
        except:
            print("ERROR libghdl initialization")

        

        # Load the file
        file_id = name_table.Get_Identifier(self.filename)
        sfe = files_map.Read_Source_File(name_table.Null_Identifier, file_id)
        if sfe == files_map.No_Source_File_Entry:
            print("ERROR cannot open file "+ self.filename)
            quit()

        # Parse file
        try:
            self.file = sem_lib.Load_File(sfe)
            if self.file == nodes.Null_Iir:
                sys.exit(1)
        except:
            print("ERROR parsing file "+ self.filename)
       

########################
### Global functions
########################

    def DisplayGenInfo(self,node):
        """Return General information regarding the node name line-column"""
        return str(self.getIdentifier(node)) + "("+str(self.getNodeLineInFile(node)) + ":"+ str(self.getNodeColumInFile(node))+ ")"
    

    def DisplayNodeInfo(self,node) -> str:
        """Return General information regarding the node"""
        return self.GetNodeType(node)+ str(self.DisplayGenInfo(node))
    

    def GetNodeType (self,node) -> str:
        """Return the name of the node type"""
        if nodes.Get_Kind(node) == nodes.Iir_Kind.Design_Unit:
            return "Design name: "
        elif nodes.Get_Kind(node) == nodes.Iir_Kind.Entity_Declaration:
            return "Entity name: "
        elif  nodes.Get_Kind(node) == nodes.Iir_Kind.Interface_Signal_Declaration:
            return "Entity Interface port name: "
        elif nodes.Get_Kind(node) == nodes.Iir_Kind.Architecture_Body:
            return "Architecture name: "
        elif nodes.Get_Kind(node) == nodes.Iir_Kind.Constant_Declaration:
            return "Constant declaration name: "
        elif nodes.Get_Kind(node) == nodes.Iir_Kind.Signal_Declaration:
            return "Signal declaration name: "    
        else :
            return "Unknown-Untested type: "

    def getIdentifier(self,node):
        """Return the Python string from node :obj:`node` identifier"""
        return name_table.Get_Name_Ptr(nodes.Get_Identifier(node))

    def getNodeLineInFile (self,node):
        """ Return the line in original file of the node :obj:`node` """
        loc = nodes.Get_Location(node)
        fil = files_map.Location_To_File(loc)
        pos = files_map.Location_File_To_Pos(loc, fil)
        line = files_map.Location_File_To_Line(loc, fil)
        return line

    def getNodeColumInFile (self,node):
        """ Return the column in original file of the node :obj:`node` """
        loc = nodes.Get_Location(node)
        fil = files_map.Location_To_File(loc)
        pos = files_map.Location_File_To_Pos(loc, fil)
        line = files_map.Location_File_To_Line(loc, fil)
        col = files_map.Location_File_Line_To_Offset(loc, fil, line)
        return col


########################
### Rules checked
########################
    def CNE_02500(self):
        """ Rule CNE_02500 to evaluate Length of entities name. This function report entity names."""
        # Get first node of design units
        try:
            designUnit = nodes.Get_First_Design_Unit(self.file)
        except:
            print("ERROR parsing file "+ self.filename+" for CNE_02500 rule")
            pass

        #iterate around all nodes
        while designUnit != nodes.Null_Iir:
            #analysing nodes of type library Unit
            libraryUnit = nodes.Get_Library_Unit(designUnit)
            #VHDL entity
            if nodes.Get_Kind(libraryUnit) == nodes.Iir_Kind.Entity_Declaration:
                name=self.getIdentifier(libraryUnit)
                #get entity ports names
                if nodes_meta.Has_Port_Chain(nodes.Get_Kind(libraryUnit)):
                    #print("Info: Entity has got ports")
                    for port in pyutils.chain_iter(nodes.Get_Port_Chain(libraryUnit)):
                        #get port name
                        PortName = self.getIdentifier(port)
                        #evaluate rule size
                        if self.CNE_02500_Relation =="LT":
                            if not (len(PortName)<int(self.CNE_02500_Value)):
                                print(self.DisplayGenInfo(port))
                        elif self.CNE_02500_Relation =="LET":
                            if not (len(PortName)<=int(self.CNE_02500_Value)):
                                print(self.DisplayGenInfo(port))
                        else:
                            #others parameters are not relevant for this rule
                            print("CNE_02500 parameter error. E,GT and GET are not relevant for this rule")

            #go to next node
            designUnit = nodes.Get_Chain(designUnit)

    def CNE_02600(self):
        """ Rule CNE_02600 to evaluate Length of signal name. This function report signal names."""
        # Get first node of design units
        try:
            designUnit = nodes.Get_First_Design_Unit(self.file)
        except:
            print("ERROR parsing file "+ self.filename+" for CNE_02600 rule")
            pass

        while designUnit != nodes.Null_Iir:
            #analysing nodes of type library Unit
            libraryUnit = nodes.Get_Library_Unit(designUnit)

            #VHDL Architecture    
            if nodes.Get_Kind(libraryUnit) == nodes.Iir_Kind.Architecture_Body:
                # get list of declarations
                if nodes_meta.Has_Declaration_Chain(nodes.Get_Kind(libraryUnit)):
                    #print("Info: Architecture  has got declarations")
                    #get every architecture declarations
                    for Declarations in pyutils.declarations_iter(libraryUnit):
                        #get signal name
                        Signame = self.getIdentifier(Declarations)
                        #evaluate rule size
                        if self.CNE_02600_Relation =="LT":
                            if not (len(Signame)<int(self.CNE_02600_Value)):
                                print(self.DisplayGenInfo(Declarations))
                        elif self.CNE_02600_Relation =="LET":
                            if not (len(Signame)<=int(self.CNE_02600_Value)):
                                print(self.DisplayGenInfo(Declarations))
                        else:
                            #others parameters are not relevant for this rule
                            print("CNE_02500 parameter error. E,GT and GET are not relevant for this rule")

            #go to next node
            designUnit = nodes.Get_Chain(designUnit)
