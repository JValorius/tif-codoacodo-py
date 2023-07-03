const { createApp } = Vue;

const customHeader = {
    template: `
            <div class="branding-sitio upper">
                <a href="index.html" rel="home" title="Elegir Clínica">
                    <div><img src="svg/isologo.svg" height="50" alt="ElegirClinica Logo"></div>
                </a>
                <div class="descripcion-container">
                    <h4 class="descripcion-sitio">{{tagline}}</h4>
                </div>
            </div>
            <div aria-hidden="true" id="menu-principal" class="menu nav-menu">
                <a v-bind:href="ranking" id="menu-princ-2" class="menu-item">Clínicas</a>
                <a v-bind:href="analysis" id="menu-princ-3" class="menu-item">Ratings</a>
                <a v-bind:href="about" id="menu-princ-4" class="menu-item">Usuarios</a>
                <a href="javascript:void(0);" id="menu-hamburg" class="hamburguesa" onclick="abrirMenu()">
                    <i class="fa fa-bars"></i>
                </a>
            </div>
        `,
    data() {
        return {
            tagline: 'Panel de control',
            Clínicas: "clinicas.html",
            Ratings: "ratings.html",
            Usuarios: "usuarios.html",
        }
    },
};

const customFooter = {
    template: `
            <div class="branding-sitio lower">
                <div class="bottom-logo"><img src="svg/logo.svg" height="50" alt="ElegirClinica Logo"></div>
                <div class="info-sitio">
                    <ul>
                        <li>Elegir Clínica</li>
                        <li>{{tagline}}</li>
                    </ul>
                </div>
            </div>
            <div class="redes">
                <a href="https://www.twitter.com" target="_blank" class="redsoc">
                    <i aria-hidden="true" class="fa fa-twitter"></i>
                </a>
                <a href="https://www.facebook.com" target="_blank" class="redsoc">
                    <i aria-hidden="true" class="fa fa-facebook"></i>
                </a>
                <a href="https://www.instagram.com" target="_blank" class="redsoc">
                    <i aria-hidden="true" class="fa fa-instagram"></i>
                </a>
                </a> <a href="https://www.linkedin.com" target="_blank" class="redsoc">
                    <i aria-hidden="true" class="fa fa-linkedin"></i>
                </a>
            </div>
            <div class="copyright">
                <p>Copyright © 2023 Venture Design</p>
            </div>
        `,
    data() {
        return {
            tagline: 'Ranking de centros médicos de Buenos Aires, elaborado por sus pacientes',
        }
    },
};

const headerApp = Vue.createApp({
    components: {
        'custom-header': customHeader,
    }
}).mount('#header-index');

const footerApp = Vue.createApp({
    components: {
        'custom-footer': customFooter,
    }
}).mount('#footer-index');