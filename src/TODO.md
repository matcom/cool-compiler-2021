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
- [ ] case of
- [ ] Llamado dinamico self type
- [ ] At @
- Funciones nativas:
  - [ ] Copy
  - [ ] Length
  - [ ] Substring
  - [ ] Concat
  - [ ] TypeName?
  