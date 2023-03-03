//---------------------------------------------
//----------- DATATABLE : CONTEXT MENU --------
//---------------------------------------------

// (Réf: TONTEXT-MENU-000)

/**{% load static %}
Le context-menu s'affiche exacetment {% load static %}sur les coordonnées de la souris ie du coté haut-gauche du context menu
Le context-menu s'affiche partout tan{% load static %}t que le souris reste sur les rows et cols.
Click sur un élément du context-menu {% load static %}fait appel à une action externe définit sur chaque table appellante d'ou la 
présence du dropdown juste en bas de la déclaration de la table (voir les listes.html).

ATTENTION: La page doit être rechargée pour faire apparaître le contex-tmenu. ceci est déja fait automatiquement
au niveau de python. IL FAUT CONTINUER LA RECHERCHE ...

*/

/**
 * Fonction permettant de gerer la position d'affichage du context-menu par rapport au document
 * @param {} e 
 */
function getPosition(e) {
    var posx = 0;
    var posy = 0;

    if (!e) var e = window.event;

    // Position par défaut
    posx = e.pageX - 57;
    posy = e.pageY - 64;
    
    // Largeur et Hauteur du browser
    windowWidth = $(window).width(); 
    windowHeight = $(window).height();
    
    // Largeur et hauteur du context-menu
    var W =  $("#context-menu").width();
    var L =  $("#context-menu").height();

    // Dépassement vers la droite
    if ( (W + e.clientX) > windowWidth ) {
        // console.log('x is outside');
        posx = e.clientX - W - 57;
    }

    // Dépassement vers la gauche
    if ( posx < 0 ){
        posx = 0;
    }

    // hauteur de la barre de tache de l'applciation
    var Hb = 50; //50px

    // Dépassement vers le bas
    if ( (L + e.clientY) > windowHeight - Hb) {
        // console.log('y is outside');
        posy = e.clientY - L - 64;
    }
    
    // Dépassement vers le hau$(document).ready(function(){t
    if ( posy < 0 ){
        posy = 0;
    }

    //console.log('x: '+ posx +', y: ' + posy);

    // Renvoyer la nouvelle position appropriée
    return {
        x: posx,
        y: posy
    }
}

// Définition du context menu quis'affiche uniquement sur une ligne du datatable
$('tr').on('contextmenu', function(e) {
    // Lire la valeur de la première et deuxiéme colone de la ligne seléctionné
    var Libelle =  $(this).children('td:first').text();
    if ( $(this).find('td').eq(1) ) {
        Libelle += ' - ' + $(this).find('td').eq(1).text();
    }
    // Afficher cette valeur (30 maximum) # FRED 20210417
    $("#tr_current").text(Libelle.substring(0, 30) + "...");

    e.preventDefault();

    // Si le rowindex = 0 alors ne pas afficher le context-menu
    var row_index = $(this).parent().index();
    if (row_index == 0) {
        $("#context-menu").removeClass("show").hide();
        return false;
    }

    // Lire la dernière column qui contient l'ID de l'objet (caché par défaut) et le stocker dans OBJECT_ID
    last_col_id = $(this)[0].cells.length;
    OBJECT_ID = $(this)[0].cells.item(last_col_id - 1).innerText;

    // Lire l'avant dernière column qui contient l'ID de l'objet étrangère (2e) (caché par défaut) et le stocker dans OBJECT_ID_SECOND
    OBJECT_ID_SECOND = $(this)[0].cells.item(last_col_id - 2).innerText;

    update_data_url(OBJECT_ID, OBJECT_ID_SECOND);

    // Positionner le context-menu juste au coins gauche/droite de la souris
    coord = getPosition(e);
    var top = coord.y;
    var left = coord.x;

    $("#context-menu").css({
        display: "block",
        top: top,
        left: left,
    }).addClass("context-menu-border").addClass("show");

    return false; //bloque le right-click du browser lors du Clic droit de table

}).on("click", function() {
    $("#context-menu").removeClass("show").hide();
});

// Rendre invisible le context-menu après avoir cliqué sur un sous-menu du context-menu
$("#context-menu a").on("click", function() {
    $(this).parent().removeClass("show").hide();

    //Reinitialise le URL de l'élément 'a' en cours avec pk=0
    //$(this).attr("data-url", TD_OBJECT_URL);
    
    // Et remettre l'url original à vide  
    //TD_OBJECT_URL = "";
});

// Rendre invisible le context-menu lorsqu'on clique sur la page html
$('html').click(function() {
     $("#context-menu").removeClass("show").hide();
});

// Rendre invisible le context-menu lorsqu'on sur la touche 'ESC'
$(document).keyup(function(e) {
    if (e.key === "Escape") {
        $("#context-menu").removeClass("show").hide();
    }
});

/**
 * Générer l'url du lien qui ouvre directement un popup modal, c'est à dire le link ayant l'attribut
 * @param {identifiant de l'objet}  OBJECT_ID
 * @param {identifiant du second objet}  OBJECT_ID_SECOND
 */
function update_data_url(OBJECT_ID, OBJECT_ID_SECOND) {
    $('a.dropdown-item', '#context-menu').each(function () {
        var second_id = $(this).attr('second-id');
        var url = $(this).attr('data-url');
        var new_url = null;

        if (url) {
            //NETTOYER L'URL = RESTAURER L'URL ORIGINAL = REMETTRE À ZERO LES ENTIERS > 0
            var number = url.match(/\d+/);
            if ((number) && ($.isNumeric( number[0] ))) {
                url = url.replace(number[0], 0);
            }

            if (( second_id ) && ( $.isNumeric( OBJECT_ID_SECOND ) && ( OBJECT_ID_SECOND > 0 ) ) ) {
                // with SECONDE ID
                // S'il y a un ZERO comme /erp/rh/user/chef/equipe/0/update alors, remplacer ce zero par le OBJECT_ID
                new_url = url.replace(0, OBJECT_ID_SECOND);
            } else {
                if ( $.isNumeric( OBJECT_ID ) ) {
                    // ONLY ID
                    // S'il y a un ZERO comme /erp/rh/user/chef/equipe/0/update alors, remplacer ce zero par le OBJECT_ID
                    new_url = url.replace(0, OBJECT_ID);
                }
            }
            
            if (new_url != null) {
                // METTRE À JOUR LE URL
                $(this).attr('data-url', new_url);
                //console.log(new_url + ' salut');
            } else {
                //DESACTIVER UN POPUP (ID = 0) => TRES IMPORTANT
                var number = url.match(/\d+/);
                if ((number) && ($.isNumeric(number[0])) && (number[0] == 0) ) {
                    $(this).addClass("disabled-element");
                }
            }
        }
    });
}

/**
 * Générer l'url du lien qui ouvre directement une page, c'est à dire le link ayant l'attribut onfocus="update_href(this);"
 * @param {identifiant de l'objet} a_link
 */
function update_href(a_link) {
    var url = $(a_link).attr("data-url");
    // Sauvegarder l'url original avec pk=0
    TD_OBJECT_URL = url;
    
    //Mettre à jour le nouveau url
    new_url = url;//.replace(999, OBJECT_ID);

    //Modifier le href de l'élément du menu 'a'
    $(a_link).attr("href", new_url);
    
    // Forcer l'ouverture de la page via cet 'href'
    location.href = new_url;
    //console.log('new url = ' + new_url);
    
    return false;
}
