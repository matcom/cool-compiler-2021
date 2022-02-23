.TYPE
type Main: {
	attribute type          ->  Main
	function abort          ->  Object_abort
	function copy           ->  Object_copy
	function type_name      ->  Object_type_name
	function in_int         ->  IO_in_int
	function in_string      ->  IO_in_string
	function out_int        ->  IO_out_int
	function out_string     ->  IO_out_string
	function main           ->  Main_main
}
.DATA
	data string_0: Hello, World.

.FUNCTION
function Main_main: {
	PARAM self
	LOCAL param_0_to_out_string@0
	LOCAL @result
	Load param_0_to_out_string@0 string_0 
	Comment Fin del paramentro 0 al StaticDispatch out_string 
	Arg self 
	Comment Agrega a la pila el paramentro 0 al StaticDispatch out_string 
	Arg param_0_to_out_string@0 
	Comment Agrega a la pila el paramentro 1 al StaticDispatch out_string 
	VCall @result Main IO_out_string 
	Return @result 
	Comment Final de la function main 
}
function new_ctr_Main: {
	LOCAL instance
	LOCAL type_name@0
	LOCAL @result
	ALLOCATE instance Main 
	Comment Reservando memoria para una instancia de tipo Main 
	Load type_name@0 Main_name 
	Comment Cargando el nombre del tipo desde el data 
	SetAttr instance type type_name@0 
	Comment Assignando el nombre del tipo en el campo type 
	Arg instance 
	VCall @result Main Main_main 
	Comment Llamando al mentodo inicial del programa 
	Return 0 
}
