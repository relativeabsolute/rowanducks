# Author: Curtis Baillie
# This class holds all necessary information for each line in the report (employee)
# In the diff class, we will create an array of these objects that we will pass to
# the report generator class.


class CMS2File:

    # Declares all variables, sets initial values.
    name = ""
    type = ""
    HL_exec_stmts = 0
    HL_exec_lines = 0
    HL_data_stmts = 0
    HL_data_lines = 0
    HL_comment_stmts = 0
    HL_comment_lines = 0
    HL_noncomment_lines = 0
    HL_other_stmts = 0
    Direct_exec_stmts = 0
    Direct_data_stmts = 0
    Direct_comment_lines = 0

    Total_exec_stmts = 0
    Total_src_lines = 0

    # Constructor
    def __init__(self, name, type, HL_exec_stmts, HL_exec_lines, HL_data_stmts,
                 HL_data_lines, HL_comment_stmts, HL_comment_lines, HL_noncomment_lines,
                 HL_other_stmts, Direct_exec_stmts, Direct_data_stmts,
                 Direct_comment_lines):
        self.name = name
        self.type = type
        self.HL_exec_stmts = HL_exec_stmts
        self.HL_exec_lines = HL_exec_lines
        self.HL_data_stmts = HL_data_stmts
        self.HL_data_lines = HL_data_lines
        self.HL_comment_stmts = HL_comment_stmts
        self.HL_comment_lines = HL_comment_lines
        self.HL_noncomment_lines = HL_noncomment_lines
        self.HL_other_stmts = HL_other_stmts
        self.Direct_exec_stmts = Direct_exec_stmts
        self.Direct_data_stmts = Direct_data_stmts
        self.Direct_comment_lines = Direct_comment_lines

        self.Total_exec_stmts = HL_exec_stmts + Direct_exec_stmts
        self.Total_src_lines = HL_exec_lines + HL_data_lines + HL_comment_lines + HL_noncomment_lines + Direct_comment_lines

    def recalculateTotals(self):
        CMS2File.Total_src_lines = self.HL_exec_lines + self.HL_data_lines + self.HL_comment_lines + self.HL_noncomment_lines + self.Direct_comment_lines
        CMS2File.Total_exec_stmts = self.HL_exec_stmts + self.Direct_exec_stmts
        x = self.HL_exec_stmts + self.Direct_exec_stmts
        print "Made it to recalc Totals!"

    # Define all "getters" and "setters"
    #----------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    #----------------------------
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
    #----------------------------
    @property
    def HL_exec_stmts(self):
        return self._HL_exec_stmts

    @HL_exec_stmts.setter
    def HL_exec_stmts(self, value):
        self._HL_exec_stmts = value
        # Recalculate total exec stmts
        #self.Total_exec_stmts = self.HL_exec_stmts + self.Direct_exec_stmts
    #----------------------------
    @property
    def HL_exec_lines(self):
        return self._HL_exec_lines

    @HL_exec_lines.setter
    def HL_exec_lines(self, value):
        self._HL_exec_lines = value
        # Recalculate total src lines
        #self.Total_src_lines = self.HL_exec_lines + self.HL_data_lines + self.HL_comment_lines + self.HL_noncomment_lines + self.Direct_comment_lines

    #----------------------------
    @property
    def HL_data_stmts(self):
        return self._HL_data_stmts

    @HL_data_stmts.setter
    def HL_data_stmts(self, value):
        self._HL_data_stmts = value
    #----------------------------
    @property
    def HL_data_lines(self):
        return self._HL_data_lines

    @HL_data_lines.setter
    def HL_data_lines(self, value):
        self._HL_data_lines = value
        # Recalculate total src lines
        #self.Total_src_lines = self.HL_exec_lines + self.HL_data_lines + self.HL_comment_lines + self.HL_noncomment_lines + self.Direct_comment_lines
    #----------------------------
    @property
    def HL_comment_stmts(self):
        return self._HL_comment_stmts

    @HL_comment_stmts.setter
    def HL_comment_stmts(self, value):
        self._HL_comments_stmts = value
    #----------------------------
    @property
    def HL_comment_lines(self):
        return self._HL_comment_lines

    @HL_comment_lines.setter
    def HL_comment_lines(self, value):
        self._HL_comments_lines = value
        # Recalculate total src lines
        #self.Total_src_lines = self.HL_exec_lines + self.HL_data_lines + self.HL_comment_lines + self.HL_noncomment_lines + self.Direct_comment_lines
    #----------------------------
    @property
    def HL_noncomment_lines(self):
        return self._HL_noncomment_lines

    @HL_noncomment_lines.setter
    def HL_noncomment_lines(self, value):
        self._HL_noncomment_lines = value
        # Recalculate total src lines
        #self.Total_src_lines = self.HL_exec_lines + self.HL_data_lines + self.HL_comment_lines + self.HL_noncomment_lines + self.Direct_comment_lines
    #----------------------------
    @property
    def HL_other_stmts(self):
        return self._HL_other_stmts
    @HL_other_stmts.setter
    def HL_other_stmts(self, value):
        self._HL_other_stmts = value

    # ----------------DIRECT---------------------
    @property
    def Direct_exec_stmts(self):
        return self._Direct_exec_stmts

    @Direct_exec_stmts.setter
    def Direct_exec_stmts(self, value):
        self._Direct_exec_stmts = value
        # Recalculate total exec stmts
        #self.Total_exec_stmts = self.HL_exec_stmts + self.Direct_exec_stmts
        self.recalculateTotals()
    #----------------------------
    @property
    def Direct_data_stmts(self):
        return self._Direct_data_stmts
    @Direct_data_stmts.setter
    def Direct_data_stmts(self, value):
        self._Direct_data_stmts = value
    #----------------------------
    @property
    def Direct_comment_lines(self):
        return self._Direct_comment_lines
    @Direct_comment_lines.setter
    def Direct_comment_lines(self, value):
        self._Direct_comments_lines = value
        # Recalculate total src lines
        #self.Total_src_lines = self.HL_exec_lines + self.HL_data_lines + self.HL_comment_lines + self.HL_noncomment_lines + self.Direct_comment_lines
        recalculateTotals()

    #TODO: Optimize recalculation of src/exec lines by writing a method and calling it when necessary.

    # ------------------TOTAL--------------------

    # -------------------END---------------------