from typing import List, Union, Tuple, Optional, Dict
from collections import OrderedDict


class SQL:

    def __init__(self, names: List[str], columns: List[int]):
        self.tables = {}
        for (name, cols) in zip(names, columns):
            self.tables[name] = {
                'cols': cols,
                'last_id': 0,
                'table': OrderedDict()
            }

    def ins(self, name: str, row: List[str]) -> bool:
        """
        Insert a row in a specific table with an id assigned using an auto-increment method, where the id of the first
        inserted row is 1, and the id of each new row inserted into the same table is one greater than the id of the
        last inserted row, even if the last row was removed.
        :param name:
        :param row:
        :return:
        """
        if name not in self.tables.keys():
            # name does not exist in our tables
            return False

        table_meta = self.tables[name]
        cols = table_meta['cols']
        if len(row) != cols:
            # the number of columns does not match
            return False

        # update the last id and insert this new row
        table = table_meta['table']
        table_meta['last_id'] += 1
        table[table_meta['last_id']] = row

        return True

    def rmv(self, name: str, rowId: int) -> None:
        """
        Remove a row from a specific table. Removing a row does not affect the id of the next inserted row.
        :param name:
        :param rowId:
        :return:
        """
        if name not in self.tables.keys():
            # name does not exist in our tables
            return

        table = self.tables[name]['table']
        if rowId not in table.keys():
            # the specified rowId does not exist
            return

        # delete the row
        del table[rowId]

        return

    def sel(self, name: str, rowId: int, columnId: int) -> str:
        """
        Select a specific cell from any table and return its value.
        :param name:
        :param rowId:
        :param columnId:
        :return:
        """
        if name not in self.tables.keys():
           # name does not exist in our tables
            return "<null>"

        columnId -= 1
        if columnId < 0 or columnId >= self.tables[name]['cols']:
            # columnId is not in a valid range
            return "<null>"

        table = self.tables[name]['table']
        if rowId not in table.keys():
            # rowId does not exist in the table
            return "<null>"

        return table[rowId][columnId]

    def exp(self, name: str) -> List[str]:
        """
        Export all rows from any table in csv format.
        :param name:
        :return:
        """
        if name not in self.tables.keys():
            # name does not exist in our tables
            return []

        ret_list = []  # our list to return
        table = self.tables[name]['table']
        for rowId, row in table.items():
            # append this row as a string with columns separated by commas
            # since it needs to be in csv (comma separated values) format
            ret_list.append(",".join([str(rowId)] + row))

        return ret_list

# Your SQL object will be instantiated and called as such:
# obj = SQL(names, columns)
# param_1 = obj.ins(name,row)
# obj.rmv(name,rowId)
# param_3 = obj.sel(name,rowId,columnId)
# param_4 = obj.exp(name)

def main():
    input_names = ["SQL","ins","sel","ins","exp","rmv","sel","exp"]
    input_args = [[["one","two","three"],[2,3,1]],["two",["first","second","third"]],["two",1,3],["two",["fourth","fifth","sixth"]],["two"],["two",1],["two",2,2],["two"]]

    sql_obj =  SQL(*input_args[0])
    print(f"Initial SQL object with: \nTables (initialized with 0 rows each): {input_args[0][0]}\nCols: {input_args[0][1]}\n")
    commands = []
    command_names = input_names[1:]
    command_args = input_args[1:]

    for i in range(1, len(input_names)):
        # curate the commands that will be run
        command_name = input_names[i]
        if command_name == "ins":
            commands.append(sql_obj.ins)
        elif command_name == "rmv":
            commands.append(sql_obj.rmv)
        elif command_name == "sel":
            commands.append(sql_obj.sel)
        elif command_name == "exp":
            commands.append(sql_obj.exp)
        else:
            raise NotImplementedError(f"Command {command_name} not implemented.")

    for i in range(len(commands)):
        print(f"Command {i} ({command_names[i]}): {commands[i]}")
        print(f"Command args: {command_args[i]}")
        result = commands[i](*command_args[i])
        print(f"Result: {result}\n")

if __name__ == '__main__':
    main()