var id = location.search.substring(4); // Obtiene el valor del argumento 'id' de la URL
console.log(id);
const { createApp } = Vue;

createApp({
	data() {
		return {
			// Inicializa las variables
			id: 0,
			nombre: "",
			financ: "",
			direccion: "",
			localidad: "",
			telefono: "",
			website: "",
			imagen: "",
			avg_ratings: {
				promedio_inst: 0,
				promedio_medi: 0,
				promedio_serv: 0
			  },
			//url: 'http://localhost:5000/clinicas/' + id,
			url: "https://jvalorius.pythonanywhere.com/clinicas/" + id,
		};
	},
	methods: {
		fetchData(url) {
			/* Este código define un método llamado fetchData(url) que realiza una solicitud a través de fetch a una URL especificada y procesa la respuesta.
			Este código utiliza la función fetch para realizar una solicitud HTTP a una URL específica. Luego, encadena una serie de promesas utilizando los métodos then y catch.
			En el primer then, se convierte la respuesta en formato JSON mediante response.json(). Luego, en el segundo then, se accede a los datos obtenidos y se asignan a las propiedades de la instancia de Vue.
			Si se produce algún error durante el proceso, el código captura la excepción en el bloque catch y registra el error en la consola, además de establecer la propiedad error en true.
			En resumen, este código realiza una solicitud a una URL, espera la respuesta en formato JSON y actualiza los datos de la instancia de Vue con los valores obtenidos de la respuesta.
			*/
			fetch(url)
				.then((response) => response.json())
				.then((data) => {
					this.id = data.id;
					this.nombre = data.nombre;
					this.financ = data.financ;
					this.direccion = data.direccion;
					this.localidad = data.localidad;
					this.telefono = data.telefono;
					this.website = data.website;
					this.imagen = data.imagen;
				})
				.catch((err) => {
					console.error(err);
					this.error = true;
				});
		},
		modificar() {
			/* Este código define la función modificar(). En esta función, se crea un objeto clinica que contiene las propiedades nombre, precio, stock e imagen obtenidas de la instancia de Vue. Luego se define un objeto options que especifica las opciones para la solicitud HTTP.
			A continuación, se utiliza la función fetch para realizar una solicitud HTTP tipo PUT a la URL this.url utilizando las opciones definidas en options. Si la solicitud se realiza con éxito, se muestra una alerta indicando que el registro ha sido actualizado y se redirige al usuario a la página "./clinicas.html". Si ocurre algún error durante el proceso, se captura la excepción en el bloque catch, se registra el error en la consola y se muestra una alerta indicando que ha ocurrido un error al actualizar.
			 */
			let clinica = {
				nombre: this.nombre,
				financ: this.financ,
				direccion: this.direccion,
				localidad: this.localidad,
				telefono: this.telefono,
				website: this.website,
				imagen: this.imagen,
			};
			var options = {
				body: JSON.stringify(clinica),
				method: "PUT",
				headers: { "Content-Type": "application/json" },
				redirect: "follow",
			};
			fetch(this.url, options)
				.then(function () {
					alert("Registro actualizado!");
					window.location.href = "./clinicas.html";
				})
				.catch((err) => {
					console.error(err);
					alert("Error al actualizar.");
				});
		},
	},
	created() {
		/* Este código define el bloque created() en el cual se llama a la función fetchData(this.url) al crear la instancia de Vue. La función fetchData() se encarga de realizar una solicitud HTTP a la URL especificada en this.url y obtener los datos necesarios para la aplicación.
		 */
		this.fetchData(this.url);
	},
	/* Posteriormente, se utiliza el método mount("#app") para montar la instancia de Vue en el elemento HTML con el id "app". Esto permite que la instancia de Vue controle y renderice el contenido dentro de ese elemento HTML.
	*/
}).mount("#app");