/*
    Pour fonctionner ce script a besoin de 3 variables définies au préalable

        - idField : String de l'id de l'input contenant la valeur dont les fields dépendent
        - changeableFields : Array de Strings qui regroupe la totalité des fields qui dépende de idField
        - specificFields : Objet où chaque clef donne un Array de Strings contenant les id des fields a montrer si on fait ce choix

    Exemple :

        let idField = '#id_type_bien';
        let changeableFields = ['#div_id_room_amount', '#div_id_nb_etage', '#div_id_situe_etage']
        let specificFields = {
            'Garage': [],
            'Appartement': ['#div_id_room_amount', '#div_id_situe_etage'],
            'Maison': ['#div_id_room_amount', '#div_id_nb_etage']
        }
*/

// function that hides/shows field_four based upon field_three value
function check_field_value() 
{
    for (let compt = 0; compt < changeableFields.length; compt++) 
    {
        if ( specificFields[$(this).val()].includes(changeableFields[compt]) ) 
        {
            $(changeableFields[compt]).attr('style', '');
        }
        else 
        {
            $(changeableFields[compt]).attr('style', 'display: none !important;');
        }
    }
}

// this is executed once when the page loads
$(document).ready(function() {
    // set things up so my function will be called when field_three changes
    $(idField).change(check_field_value);
    // set the state based on the initial values
    check_field_value.call($(idField).get(0));
});