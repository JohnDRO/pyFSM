# pyFSM
Converts a FSM (described into a JSON file) into synthesizable code (HDL).

Here is an basic FSM example : 

![a basic FSM](http://i.imgur.com/2GbAZ8d.png)

The equivalent JSON description is this one : 

	{
		"Name": "BasicFSM",
		"InitalState": "State1",
		"Modules": {
			"Inputs": {
				"a": {
					"type": "std_logic"
				},
				"b": {
					"type": "std_logic"
				}
			},
			"Outputs": {
				"c": {
					"type": "std_logic"
				}
			},
			"States": {
				"State1": {
					"Transition": {
						"State2": {
						"condition": "a = '1'"
						}
					},
					"OutputState": {
						"c": {
						"state": "'0'"
						}
					}
				},
				"State2": {
					"Transition": {
						"State1": {
						"condition": "b = '0'"
						}
					},
					"OutputState": {
						"c": {
						"state": "'1'"
						}
					}
				}
			}
		}
	}

The goal of pyFSM is to translate this FSM code into a synthesizable code like this one (VHDL) : 

	library IEEE;
	use IEEE.std_logic_1164.all;

	entity BasicFSM is
		port (	clock : IN std_logic;  
					reset : IN std_logic;  

					a : IN std_logic;
					b : IN std_logic;

					c : OUT std_logic
		);
	end entity;

	architecture fsm of BasicFSM is
		type state_type is (State2, State1);
		signal state : state_type := State1;
	begin
		process (clock, reset)
		begin
			if (reset = '1') then
				state <= State1;
			elsif (rising_edge(clock)) then
				case state is
					when State2 =>
						if b = '0' then 
							state <= State1;
						end if;
					when State1 =>
						if a = '1' then 
							state <= State2;
						end if;
					when others =>
						state <= State1;
				end case;
			end if;
		end process;  

		process (state)
		begin
			case state is
				when State2 =>
					c <= '1';
				when State1 =>
					c <= '0';
			end case;
		end process;
	end fsm;

The idea is to firstly build a python script able to translate the JSON into some HDL. Then to build a GUI to easily draw FSM.

JSON -> VHDL : Ok
