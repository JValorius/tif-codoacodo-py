var id = location.search.substring(12); // Obtiene el valor del argumento 'id' de la URL
console.log(id);
const { createApp } = Vue;

// Crea una instancia de la aplicación Vue
createApp({
	data() {
		/* El código define una instancia de la aplicación Vue. Aquí se especifican los datos utilizados por la aplicación, incluyendo la lista de clínicas, la URL del backend, indicadores de error y carga, así como los atributos para almacenar los valores del formulario de clínicas.
		 */
		return {
			ratings: [], // Almacena las clínicas obtenidas del backend
			url: 'http://localhost:5000/ratings' + (id ? '/filter?id_clinica=' + id : ''), // URL local
			// url: "https://jvalorius.pythonanywhere.com/clinicas", // URL del backend donde se encuentran las clinicas
			error: false,
			cargando: true,
			// Atributos para el almacenar los valores del formulario
			id: 0,
			tipo: "",
			valor: 0,
			id_user: 0,
			id_clinica: 0,
			tituloPagina: "Ratings",
		};
	},
	methods: {
		fetchData(url) {
			/**El método fetchData realiza una solicitud HTTP utilizando la función fetch a la URL especificada. Luego, los datos de respuesta se convierten en formato JSON y se asignan al arreglo clínicas. Además, se actualiza la variable cargando para indicar que la carga de clínicas ha finalizado. En caso de producirse un error, se muestra en la consola y se establece la variable error en true.
			**/
			fetch(url)
				.then((response) => response.json()) // Convierte la respuesta en formato JSON
				.then((data) => {
					// Asigna los datos de las clinicas obtenidos al arreglo 'clinicas'
					this.ratings = data;
					this.cargando = false;
				})
				.catch((err) => {
					console.error(err);
					this.error = true;
				});
		},
		eliminar(rating) {
			/* El método eliminar toma un parámetro clinica y construye la URL para eliminar esa clinica en particular. Luego, realiza una solicitud fetch utilizando el método HTTP DELETE a la URL especificada. Después de eliminar la clinica, la página se recarga para reflejar los cambios.
			 */
			// Construye la URL para eliminar la clinica especificada
			const url = this.url + "/" + rating;
			var options = {
				method: "DELETE", // Establece el método HTTP como DELETE
			};
			fetch(url, options)
				.then((res) => res.text()) // Convierte la respuesta en texto (or res.json())
				.then((res) => {
					location.reload(); // Recarga la página actual después de eliminar la clinica
				});
		},
		grabar() {
			/* El método grabar se encarga de guardar los datos de una nueva clinica en el servidor. Primero, se crea un objeto clinica con los datos ingresados en el formulario. Luego, se configuran las opciones para la solicitud fetch, incluyendo el cuerpo de la solicitud como una cadena JSON, el método HTTP como POST y el encabezado Content-Type como application/json. Después, se realiza la solicitud fetch a la URL especificada utilizando las opciones establecidas. Si la operación se realiza con éxito, se muestra un mensaje de éxito y se redirige al usuario a la página de clinicas. Si ocurre algún error, se muestra un mensaje de error.
			 */
			// Crear un objeto 'clinica' con los datos del formulario
			let rating = {
				tipo: this.tipo,
				valor: this.valor,
				id_user: this.id_user,
				id_clinica: this.id_clinica,
			};

			// Configurar las opciones para la solicitud fetch
			var options = {
				body: JSON.stringify(rating), // Convertir el objeto a una cadena JSON
				method: "POST", // Establecer el método HTTP como POST
				headers: { "Content-Type": "application/json" },
				redirect: "follow",
			};

			// Realizar una solicitud fetch para guardar la clinica en el servidor
			fetch(this.url, options)
				.then(function () {
					alert("Registro grabado!");
					window.location.href = "./ratings.html"; // Redirigir a la página de clinicas
				})
				.catch((err) => {
					console.error(err);
					alert("Error al Grabar.");
				});
		},
		buscar(id) {
			this.error = false;
			var textoBuscado = this.$refs.formBusq.value;
			console.log(textoBuscado)
			if(textoBuscado && textoBuscado!="") {
				this.cargando = true;
				fetch(this.url + "/filter?term=" + textoBuscado)
					.then((res) => res.json())
					.then((data) => {
							// Mostrar los productos que coinciden con el término de búsqueda
						this.ratings = data;
						this.cargando = false;
						this.tituloPagina = "Ratings para la clínica con ID" + textoBuscado;
					})
					.catch((err) => {
						console.error(err);
						this.error = true;
						alert("Error al buscar ratings.");
					});
			} else {
				this.tituloPagina = "Ratings";
				this.fetchData(this.url);
			}
		}
	},
	created() {
		this.fetchData(this.url);
	},
}).mount("#app");