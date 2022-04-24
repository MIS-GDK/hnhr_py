def add_single_quotes(address, filename):
    with open(address + "/" + filename, "r", encoding="UTF-8") as f:
        lines = f.readlines()
    with open(address + "/" + filename, "w", encoding="UTF-8") as f:
        for i in range(len(lines)):
            if i != len(lines) - 1:
                # a = lines[i].strip() + ","
                a = "'" + lines[i].strip() + "',"
                # a = "grant select on hrhnprod." + lines[i].strip() + " to HRHNRYSC;"
            else:
                # a = lines[i].strip()
                a = "'" + lines[i].strip() + "'"
                # a = "grant select on hrhnprod." + lines[i].strip() + " to HRHNRYSC;"
            f.write(a)
            f.write("\n")


add_single_quotes("C:/Users/Administrator/Desktop", "1.txt")
