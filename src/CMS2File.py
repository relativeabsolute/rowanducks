# Author: Curtis Baillie
# This class holds all necessary information for each line in the report (employee)
# In the diff class, we will create an array of these objects that we will pass to
# the report generator class.


class CMS2File:

    def __init__(self, name, file_info):
        self.name = name
        self.total_src_lines = file_info["Number of Lines"]
        self.goto_stmts = file_info["Go-To Statements"]
        self.notes = file_info["Notes"]
        self.block_comments = file_info["Block comments"]
        self.block_comment_lines = file_info["Block comment lines"]
        self.hl_noncomment_lines = file_info["Number of non-comments"]
        self.hl_exec_stmts = file_info["HL Executable Statements"]
        self.hl_exec_lines = file_info["Lines of Multi-line High Level CMS2 Statements"]
        self.hl_data_stmts = file_info["Lines containing High Level Data Statements"]
        self.direct_exec_stmts = file_info["Direct Executable CMS2 Statements"]
        self.direct_comments = file_info["Single line Direct CMS2 comments"]
        self.hl_single_line_stmt_counter = file_info["High Level CMS2 Single Line Statements"]
        self.hl_multi_line_stmt_counter = file_info["Multi-line High Level CMS2 Statements"]
        self.total_exec_stmts = self.hl_exec_stmts + self.direct_exec_stmts
        self.hl_data_lines = 0

    def recalculate_totals(self):
        CMS2File.total_src_lines = self.hl_exec_lines + self.hl_data_lines + self.hl_noncomment_lines
        CMS2File.total_exec_stmts = self.hl_exec_stmts + self.direct_exec_stmts
        print("Made it to recalc totals!")

    # Define all "getters" and "setters"
    # ----------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    # ----------------------------

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
    # ----------------------------

    @property
    def hl_exec_stmts(self):
        return self._hl_exec_stmts

    @hl_exec_stmts.setter
    def hl_exec_stmts(self, value):
        self._hl_exec_stmts = value
        # Recalculate total exec stmts
        # self.Total_exec_stmts = self.hl_exec_stmts + self.Direct_exec_stmts
    # ----------------------------

    @property
    def hl_exec_lines(self):
        return self._hl_exec_lines

    @hl_exec_lines.setter
    def hl_exec_lines(self, value):
        self._hl_exec_lines = value
        # Recalculate total src lines
        # self.Total_src_lines = self.hl_exec_lines + self.hl_data_lines + self.hl_comment_lines + self.hl_noncomment_lines + self.Direct_comment_lines

    # ----------------------------
    @property
    def hl_data_stmts(self):
        return self._hl_data_stmts

    @hl_data_stmts.setter
    def hl_data_stmts(self, value):
        self._hl_data_stmts = value
    # ----------------------------

    @property
    def hl_data_lines(self):
        return self._hl_data_lines

    @hl_data_lines.setter
    def hl_data_lines(self, value):
        self._hl_data_lines = value
        # Recalculate total src lines
        # self.Total_src_lines = self.hl_exec_lines + self.hl_data_lines + self.hl_comment_lines + self.hl_noncomment_lines + self.Direct_comment_lines
    # ----------------------------


    @property
    def hl_noncomment_lines(self):
        return self._hl_noncomment_lines

    @hl_noncomment_lines.setter
    def hl_noncomment_lines(self, value):
        self._hl_noncomment_lines = value
        # Recalculate total src lines
        # self.Total_src_lines = self.hl_exec_lines + self.hl_data_lines + self.hl_comment_lines + self.hl_noncomment_lines + self.Direct_comment_lines
    # ----------------------------

    @property
    def hl_other_stmts(self):
        return self._hl_other_stmts

    @hl_other_stmts.setter
    def hl_other_stmts(self, value):
        self._hl_other_stmts = value

    # ----------------DIRECT---------------------
    @property
    def direct_exec_stmts(self):
        return self._direct_exec_stmts

    @direct_exec_stmts.setter
    def direct_exec_stmts(self, value):
        self._direct_exec_stmts = value
        # Recalculate total exec stmts
        # self.Total_exec_stmts = self.hl_exec_stmts + self.Direct_exec_stmts
        # self.recalculate_totals()
    # ----------------------------

    @property
    def direct_data_stmts(self):
        return self._direct_data_stmts

    @direct_data_stmts.setter
    def direct_data_stmts(self, value):
        self._direct_data_stmts = value
    # ----------------------------

    def print_string(self):
        string = "Number of Lines: " + str(self.total_src_lines) + "\n"
        string += "Go-To Statements: " + str(self.goto_stmts) + "\n"
        string += "Notes: " + str(self.notes) + "\n"
        string += "Block comments: " + str(self.block_comments) + "\n"
        string += "Block comment lines: " + str(self.block_comment_lines) + "\n"
        string += "Number of non-comments: " + str(self.hl_noncomment_lines) + "\n"
        string += "High Level CMS2 Single Line Statements: " + str(self.hl_single_line_stmt_counter) + "\n"
        string += "Multi-line High Level CMS2 Statements: " + str(self.hl_multi_line_stmt_counter) + "\n"
        string += "Lines containing High Level Data Statements: " + str(self.hl_data_stmts) + "\n"
        string += "High Level Executable Statements: " + str(self.hl_exec_stmts) + "\n"
        string += "Direct Executable Statements: " + str(self.direct_exec_stmts) + "\n"
        string += "Direct Comments: " + str(self.direct_comments) + "\n"
        string += "Total Executable Statements: " + str(self.total_exec_stmts) + "\n"
        return string

    # TODO: Optimize recalculation of src/exec lines by writing a method and calling it when necessary.

    # ------------------TOTAL--------------------

    # -------------------END---------------------
