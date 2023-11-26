class Main inherits IO {
    main() : AUTO_TYPE {
		if "Hello" = "Hello" then 
			if "0" = "1" then
				out_string("Mal1")
			else if 5 = 4 then
					out_string("Mal2")
				else if 1 = 1 then
						if new Object = new Object then
							out_string("Mal")
						else if self = self then
								out_string("Bien")
							else 
								out_string("Mal")
							fi
						fi
					else
						out_string("Mal3") 
					fi 
				fi 
			fi
		else
			out_string("Mal4") 
		fi
    };
};
