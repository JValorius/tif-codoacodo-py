const { createApp } = Vue;

// Crea una instancia de la aplicación Vue
createApp({
  data() {
    /* El código define una instancia de la aplicación Vue. Aquí se especifican los datos utilizados por la aplicación, incluyendo la lista de clínicas, la URL del backend, indicadores de error y carga, así como los atributos para almacenar los valores del formulario de clínicas.
     */
    return {
      clinicas: [], // Almacena las clínicas obtenidas del backend
      url:'http://localhost:5000/clinicas', // URL local
      // url: "https://jvalorius.pythonanywhere.com/clinicas", // URL del backend donde se encuentran los productos
      error: false,
      cargando: true,
      // Atributos para el almacenar los valores del formulario
      id: 0,
      nombre: "",
      financ: "",
      direccion: "",
      localidad: "",
      telefono: "",
      website: "",
      imagen: "",
      rt_instalaciones: 0,
      rt_medicos: 0,
      rt_servicios: 0,
      imagen: "",
    };
  },
  methods: {
    fetchData(url) {
      /**El método fetchData realiza una solicitud HTTP utilizando la función fetch a la URL especificada. Luego, los datos de respuesta se convierten en formato JSON y se asignan al arreglo clínicas. Además, se actualiza la variable cargando para indicar que la carga de clínicas ha finalizado. En caso de producirse un error, se muestra en la consola y se establece la variable error en true.
      **/
      fetch(url)
        .then((response) => response.json()) // Convierte la respuesta en formato JSON
        .then((data) => {
          // Asigna los datos de los productos obtenidos al arreglo 'productos'
          this.clinicas = data;
          this.cargando = false;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
    },
    eliminar(clinica) {
      /* El método eliminar toma un parámetro clinica y construye la URL para eliminar esa clinica en particular. Luego, realiza una solicitud fetch utilizando el método HTTP DELETE a la URL especificada. Después de eliminar la clinica, la página se recarga para reflejar los cambios.
       */
      // Construye la URL para eliminar la clinica especificada
      const url = this.url + "/" + clinica;
      var options = {
        method: "DELETE", // Establece el método HTTP como DELETE
      };
      fetch(url, options)
        .then((res) => res.text()) // Convierte la respuesta en texto (or res.json())
        .then((res) => {
          location.reload(); // Recarga la página actual después de eliminar el producto
        });
    },
    grabar() {
      /* El método grabar se encarga de guardar los datos de un nuevo producto en el servidor. Primero, se crea un objeto producto con los datos ingresados en el formulario. Luego, se configuran las opciones para la solicitud fetch, incluyendo el cuerpo de la solicitud como una cadena JSON, el método HTTP como POST y el encabezado Content-Type como application/json. Después, se realiza la solicitud fetch a la URL especificada utilizando las opciones establecidas. Si la operación se realiza con éxito, se muestra un mensaje de éxito y se redirige al usuario a la página de productos. Si ocurre algún error, se muestra un mensaje de error.
       */
      // Crear un objeto 'producto' con los datos del formulario
      let producto = {
        nombre: this.nombre,
        precio: this.precio,
        stock: this.stock,
        imagen: this.imagen,
      };

      // Configurar las opciones para la solicitud fetch
      var options = {
        body: JSON.stringify(producto), // Convertir el objeto a una cadena JSON
        method: "POST", // Establecer el método HTTP como POST
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };

      // Realizar una solicitud fetch para guardar el producto en el servidor
      fetch(this.url, options)
        .then(function () {
          alert("Registro grabado!");
          window.location.href = "./productos.html"; // Redirigir a la página de productos
        })
        .catch((err) => {
          console.error(err);
          alert("Error al Grabar.");
        });
    },
  },
  created() {
    this.fetchData(this.url);
  },
}).mount("#app");