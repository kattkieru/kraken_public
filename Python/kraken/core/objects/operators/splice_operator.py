"""Kraken - objects.operators.splice_operator module.

Classes:
SpliceOperator - Splice operator object.

"""

from kraken.core.objects.operators.base_operator import BaseOperator
from kraken.core.kraken_system import ks

class SpliceOperator(BaseOperator):
    """Base Operator representation."""

    __kType__ = "SpliceOperator"

    # TODO: Look in to expanding the Splice operator to be able to handle more
    # than one extension / operator. Need to change extension to extensions and
    # figure out how to differentiate the solver types per operator. Maybe have
    # an attirbute array called 'klOperators' that contains sets of what we
    # currently have setup.

    def __init__(self, name, solverTypeName, extension):
        super(SpliceOperator, self).__init__(name)

        self.solverTypeName = solverTypeName
        self.extension = extension

        # Load the Fabric Engine client and construct the RTVal for the Solver
        ks.loadCoreClient()
        ks.loadExtension('Kraken')
        ks.loadExtension(self.extension)
        self.solverRTVal = ks.constructRTVal(self.solverTypeName)
        self.args = self.solverRTVal.getArguments('KrakenSolverArg[]')

        # Initialize the inputs and outsputs based on the given args.
        for i in xrange(len(self.args)):
            arg = self.args[i]
            if arg.connectionType == 'in':
                if str(arg.dataType).endswith('[]'):
                    self.inputs[arg.name] = []
                else:
                    self.inputs[arg.name] = None
            else:
                if str(arg.dataType).endswith('[]'):
                    self.outputs[arg.name] = []
                else:
                    self.outputs[arg.name] = None

    def getSolverTypeName(self):
        """Returns the solver type name for this operator.

        Return:
        String, name of the solver type this operator uses.

        """

        return self.solverTypeName


    def getExtension(self):
        """Returns the extention this operator uses.

        Return:
        String, name of the extension this solver uses.

        """

        return self.extension

    def getSolverArgs(self):

        # Get the args from the solver KL object.
        return self.args

    def generateSourceCode(self):

        solverTypeName = self.getSolverTypeName()
        args = self.getSolverArgs()

        # Start constructing the source code.
        opSourceCode = ""
        opSourceCode += "require Kraken;\n"
        opSourceCode += "require " + self.getExtension() + ";\n\n"
        opSourceCode += "operator " + self.getName() + "(\n"

        opSourceCode += "    io " + solverTypeName + " solver,\n"

        functionCall = "    solver.solve("
        for i in xrange(len(args)):
            arg = args[i]
            # Connect the ports to the inputs/outputs in the rig.
            if arg.connectionType == 'out':
                opArgType = 'io' 
            else:
                opArgType = arg.connectionType
            opSourceCode += "    " + opArgType + " " + arg.dataType + " " + arg.name
            if i == len(args) - 1:
                opSourceCode += "\n"
            else:
                opSourceCode += ",\n"

            if i == len(args) - 1:
                functionCall += arg.name
            else:
                functionCall += arg.name + ", "

        opSourceCode += "    )\n"
        opSourceCode += "{\n"
        opSourceCode += functionCall + ");\n"
        opSourceCode += "}\n"

        return opSourceCode