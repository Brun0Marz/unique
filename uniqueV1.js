//Declare account number to use.
const account_number=1

function get_new_id(url) {
    const Http = new XMLHttpRequest();
    Http.open("GET", url_with_account,false);
    Http.send();
    resp= Http.responseText;

    resp_json=JSON.parse(resp);
    id_code_new= resp_json['id_code']


    return id_code_new
}

if (!sessionStorage.isNewSession) {

    //get id_code parameter.
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id_code = urlParams.get('id_code')


    //Formulate api query string and make query.
    const base_url='http://localhost:8000/process_id?accNum=';

    var url_with_account = base_url+account_number.toString();

    if (id_code) {
        url_with_account=url_with_account+'&id_code='+id_code
    } else {

    }


    id_code_new= get_new_id(url_with_account);

    web_url=window.location.href.split('?')[0]

    let paramString = window.location.href.split('?')[1];


    if (paramString) {
        id_string_old='id_code='+id_code.toString();
        id_string_new='id_code='+id_code_new;
        var ret = paramString.replace(id_string_old,id_string_new);
        window.history.replaceState(null, null, web_url+'?'+ret)
    } else {
            
        paramString='?'+'id_code='+id_code_new
        window.history.replaceState(null, null, web_url+paramString)
    }
} else {
    
}