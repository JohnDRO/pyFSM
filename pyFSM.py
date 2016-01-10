import json

def JsonToVHDL(json):
	vhdl_code = ""
	vhdl_code += "library IEEE;\n"
	vhdl_code += "use IEEE.std_logic_1164.all;\n"
	vhdl_code += "\n"
	vhdl_code += "entity " + data_load[0]['Name'] + " is\n"
	vhdl_code += "	port (	clock : IN std_logic;  \n"
	vhdl_code += "				reset : IN std_logic;  \n"
	vhdl_code += "\n"

	for i in data_load[0]['Modules']['Inputs']:
		vhdl_code += "				"+ i + " : IN " + data_load[0]['Modules']['Inputs'][i]['type'] +";\n"

	vhdl_code += "\n";
		
	for i in data_load[0]['Modules']['Outputs']:
		vhdl_code += "				"+ i + " : OUT " + data_load[0]['Modules']['Outputs'][i]['type'] +";\n"
	
	vhdl_code = vhdl_code[:-2];
	
	vhdl_code += "\n	);\n";
	vhdl_code += "end entity;\n";
	vhdl_code += "\n";
	vhdl_code += "architecture fsm of " + data_load[0]['Name'] + " is\n";

	vhdl_code += "	type state_type is (";

	for i in data_load[0]['Modules']['States']:
		vhdl_code += i + ", "

	vhdl_code = vhdl_code[:-2];
	vhdl_code += ");"

	vhdl_code += "\n"	
	vhdl_code += "	signal state : state_type := "+ data_load[0]['InitalState'] +";\n";
	vhdl_code += "begin\n"
	vhdl_code += "	process (clock, reset)\n"
	vhdl_code += "	begin\n"
	vhdl_code += "		if (reset = '1') then\n"
	vhdl_code += "			state <= " + data_load[0]['InitalState'] + ";\n"
	vhdl_code += "		elsif (rising_edge(clock)) then\n"
	vhdl_code += "			case state is\n"

	for i in data_load[0]['Modules']['States']:
		vhdl_code += "				when " + i + " =>\n"

		for j in data_load[0]['Modules']['States'][i]['Transition']:
			vhdl_code += "					if " + data_load[0]['Modules']['States'][i]['Transition'][j]['condition'] + " then \n"
			vhdl_code += "						state <= " + j +";\n";
			vhdl_code += "					end if;\n"

	vhdl_code += "				when others =>\n"
	vhdl_code += "					state <= " + data_load[0]['InitalState'] + ";\n"

	vhdl_code += "			end case;\n"	
	vhdl_code += "		end if;\n"	
	vhdl_code += "	end process;  \n\n"
	vhdl_code += "	process (state)\n"
	vhdl_code += "	begin\n"
	vhdl_code += "		case state is\n"

	for i in data_load[0]['Modules']['States']:
		vhdl_code += "			when " + i + " =>\n"
		
		for j in data_load[0]['Modules']['States'][i]['OutputState']:
				vhdl_code += "				" + j + " <= " + data_load[0]['Modules']['States'][i]['OutputState'][j]['state'] +";\n"
				
	vhdl_code += "		end case;\n"
	vhdl_code += "	end process;\n"
	vhdl_code += "\n"
	vhdl_code += "end fsm;"

	return vhdl_code

	
f = open('fsm.json', 'r')
data = f.read()
f.close()

data_load = json.loads(data)

vhdl_code = JsonToVHDL(data_load)

f = open('fsm.vhd', 'w')
f.write(vhdl_code)
f.close()

