# TODO

- En caso de ser posible, convertir el nodo substring, concat, length en CIL en una función agregada en CIL que luego se genera automaticamente en MIPS
- Terminar de hacer los nodos de CIL a MIPS
- Hacer Manual de CIL
  - Poner todas las instrucciones con una descripcion de lo que reciben

- Asociar a los nodos de CIL los respectivos nodos COOL que lo generan
- Asociar a los nodos de MIPS los respectivos nodos COOL que lo generan
- Formatear mejor la salida de MIPS, ponerle tabs a las funciones, por ejemplo
- Ponerle comentarios al codigo generado de CIL y MIPS basados en la informacion de los nodos COOL que los generan para poder debuguear mejor

- Ver error del test de generacion que tiene algun problema con los argumentos?

- **Probar que corran todos los programas del codegen con el interprete de CIL**.
- Separar CIL en un paquete aparte como está MIPS
- Separar COOL en un paquete aparte
- Separar paquete de integración de COOL, CIL, MIPS

- Hacer algo inteligente para eliminar generacion de variables innecesarias
- Hacer mecanismo para reducir codigo generado eliminando el codigo que no se usa o no alcanzable
- **PASAR TESTING GENERACION Locales y en Github**


## Generacion

- [x] Input/Output
- [x] Condicionales
- [x] Ciclos
- [x] Let in (Simple)
- [x] Llamado de funciones
- [x] Set y Get de Atributos
- [x] isvoid
- Funciones nativas:
  - [x] Copy
  - [x] Length
  - [x] Substring
  - [x] Concat
  - [x] TypeName
  - [ ] Copy especifico String, Int
- [x] At @
- [x] Llamado dinamico self type
- [ ] Llamar al __init del padre en el __init de los hijos.
- [ ] Cuando se hace abort se tiene que escribir un mensaje desde donde se hizo abort. Mirar is_prime en los ejemplos
- [ ] case of
- [ ] Atributos con igual nombre en clases heredadas, tienen que diferenciarse, o no, ver bien esto
- [ ] Verificar que los atributos se inicialicen correctamente en caso de que uno dependa de otro y a la hora de asiganrle valor uno no este inicializado.
- [ ] Verificar que se aborte cuando ocurre una excepcion en ejecucion. Los casos se especifican en el manual de Cool pagina 29