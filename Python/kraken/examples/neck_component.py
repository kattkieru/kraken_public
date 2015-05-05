from kraken.core.maths import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control  import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class NeckComponentGuide(Component):
    """Neck Component Guide"""

    def __init__(self, name='Neck', parent=None):
        super(NeckComponentGuide, self).__init__(name, parent)

        self.neck = Control('neck', parent=self, shape="sphere")
        self.neckEnd = Control('neckEnd', parent=self, shape="sphere")

        self.loadData({
            "name": name,
            "location": "M",
            "neckPosition": Vec3(0.0, 16.5572, -0.6915),
            "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
        })


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = {
            "name": self.getName(),
            "location": self.getLocation(),
            "neckPosition": self.neck.xfo.tr,
            "neckEndPosition": self.neckEnd.xfo.tr
            }

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        self.setName(data['name'])
        self.setLocation(data['location'])
        self.neck.xfo.tr = data['neckPosition']
        self.neckEnd.xfo.tr = data['neckEndPosition']

        return True


    def getGuideData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        # values
        neckEndPosition = self.neck.xfo.tr
        neckPosition = self.neckEnd.xfo.tr
        neckUpV = Vec3(0.0, 0.0, -1.0)

        # Calculate Neck Xfo
        rootToEnd = neckEndPosition.subtract(neckPosition).unit()
        rootToUpV = neckUpV.subtract(neckPosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()

        neckXfo = Xfo()
        neckXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, neckPosition)

        return {
                "class":"kraken.examples.hand_component.HandComponent",
                "name": self.getName(),
                "location":self.getLocation(),
                "neckXfo": neckXfo
                }


class NeckComponent(Component):
    """Neck Component"""

    def __init__(self, name="Neck", parent=None):

        Profiler.getInstance().push("Construct Neck Component:" + name)
        super(NeckComponent, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        controlsLayer = self.getOrCreateLayer('controls')
        ctrlCmpGrp = ComponentGroup(self.getName(), parent=controlsLayer)

        # IO Hierarchies
        inputHrcGrp = HierarchyGroup('inputs', parent=ctrlCmpGrp)
        cmpInputAttrGrp = AttributeGroup('inputs')
        inputHrcGrp.addAttributeGroup(cmpInputAttrGrp)

        outputHrcGrp = HierarchyGroup('outputs', parent=ctrlCmpGrp)
        cmpOutputAttrGrp = AttributeGroup('outputs')
        outputHrcGrp.addAttributeGroup(cmpOutputAttrGrp)

        # Neck
        self.neckCtrlSpace = CtrlSpace('neck', parent=ctrlCmpGrp)

        self.neckCtrl = Control('neck', parent=self.neckCtrlSpace, shape="pin")
        self.neckCtrl.scalePoints(Vec3(1.25, 1.25, 1.25))
        self.neckCtrl.translatePoints(Vec3(0, 0, -0.5))
        self.neckCtrl.rotatePoints(90, 0, 90)
        self.neckCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        defCmpGrp = ComponentGroup(self.getName(), parent=deformersLayer)

        neckDef = Joint('neck', parent=defCmpGrp)
        neckDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        self.neckEndInput = Locator('neckBase', parent=inputHrcGrp)
        self.neckEndOutput = Locator('neckEnd', parent=outputHrcGrp)
        self.neckOutput = Locator('neck', parent=outputHrcGrp)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', self.getLocation() is 'R')

        cmpInputAttrGrp.addAttribute(debugInputAttr)
        cmpInputAttrGrp.addAttribute(rightSideInputAttr)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([self.neckCtrlSpace.getName(), 'To', self.neckEndInput.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(self.neckEndInput)
        self.neckCtrlSpace.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        neckEndConstraint = PoseConstraint('_'.join([self.neckEndOutput.getName(), 'To', self.neckCtrl.getName()]))
        neckEndConstraint.addConstrainer(self.neckCtrl)
        self.neckEndOutput.addConstraint(neckEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(self.neckEndInput)
        self.addOutput(self.neckEndOutput)
        self.addOutput(self.neckOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        #Add Deformer Splice Op
        spliceOp = SpliceOperator("neckDeformerSpliceOp", "PoseConstraintSolver", "Kraken")
        self.addOperator(spliceOp)

        # Add Att Inputs
        spliceOp.setInput("debug", debugInputAttr)
        spliceOp.setInput("rightSide", rightSideInputAttr)

        # Add Xfo Inputstrl)
        spliceOp.setInput("constrainer", self.neckEndOutput)

        # Add Xfo Outputs
        spliceOp.setOutput("constrainee", neckDef)

        Profiler.getInstance().pop()


    def loadData(self, data=None):

        self.setName(data.get('name', 'Neck'))
        location = data.get('location', 'M')
        self.setLocation(location)

        self.neckCtrlSpace.xfo = data['neckXfo']
        self.neckCtrl.xfo = data['neckXfo']

        # ============
        # Set IO Xfos
        # ============
        self.neckEndInput.xfo = data['neckXfo']
        self.neckEndOutput.xfo = data['neckXfo']
        self.neckOutput.xfo = data['neckXfo']


from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(NeckComponent)
