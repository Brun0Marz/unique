console.log('script started')

//Declare account number to use.
const account_number=1

//get id_code parameter.
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const id_code = urlParams.get('id_code')
console.log(id_code)

//Formulate api query string and make query.
const Http = new XMLHttpRequest();
const base_url='http://localhost:8000/process_id?accNum=';

var url_with_account = base_url+account_number.toString();

if (id_code) {
    url_with_account=url_with_account+'&id_code='+id_code
} else {

}

console.log(url_with_account)

Http.open("GET", url_with_account);
Http.send();

Http.onreadystatechange = (e) => {
    resp=Http.responseText;
    resp_json=JSON.parse(resp);
    id_code_new=resp_json['id_code'];

    web_url=window.location.href
    
    if (id_code_new) {
        let paramString = window.location.href.split('?')[1];
        id_string_old='id_code='+id_code.toString();
        id_string_new='id_code='+id_code_new;
        var ret = paramString.replace(id_string_old,id_string_new);
        window.history.replaceState(null, null, web_url+ret)
    } else {
        var ret = paramString.replace(id_string_old,'')
        window.history.replaceState(null, null, web_url+ret);
    }
}
