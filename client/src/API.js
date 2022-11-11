const URL = "http://localhost:8000/hiketracking/"

async function createHike(hike_description, hike_file, token) {
  const valid_token = ('Token ' + token).replace('"', '').slice(0, -1)
  
  try {
    let response = await fetch(URL + 'hike/', {
      method: 'POST',
      body: JSON.stringify(hike_description),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': valid_token
      },
    })

    if (response.status == '200') {
      response = await response.json()
      let second_response = await fetch(URL + 'hike/file/' + response['hike_id'], {
        method: 'PUT',
        body: hike_file,
        headers: {
          'Authorization': valid_token
        },
      })

      if (second_response.status == '200')
        return {msg: "Hike Creato"};

        return {error: true, msg: "Qualcosa è andato storto. Verifica tutti i campi e riprova"};
    }

    return {error: true, msg: "Qualcosa è andato storto. Verifica tutti i campi e riprova"};
  }

  catch (e) {
    console.log(e) // TODO
  }
}

async function login(credentials) {
  let response = await fetch(URL + 'login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (response.status == '200')
    return { msg: await response.json() }
  else {
    return { error: 'Error', msg: "Qualcosa è andato storto nel login. Riprovare" }
  }
}

async function signin(credentials) {
  let response = await fetch(URL + 'register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (response.status == '200')
    return { msg: await response.json() }
  else {
    return { error: 'Error', msg: "Qualcosa è andato storto nella registrazione. Riprovare" }
  }

}

async function logout(token) {
  const valid_token = token = ('Token ' + token).replace('"', '').slice(0, -1)
  await fetch(URL + 'logout/', {
    method: 'POST',
    headers: {
      'Authorization': valid_token
    },
  });
}

async function getHikes(filter, userPower) {
  if (userPower !== "")
    userPower += '/'
  const response = await fetch(URL + userPower + 'hikes?filter=' + filter, { method: 'GET', credential: 'include' })
  const up = await response.json();
  if (response.ok) {
    return up;
  } else {
    throw up;
  }
}

async function getAllHikes(token) {
  const valid_token = token = ('Token ' + token).replace('"', '').slice(0, -1)
  let response = await fetch(URL + 'allhikes/', {
    method: 'GET',
    headers: {
      //'Authorization': valid_token
    },
  });

  if (response.status == '200')
    return { msg: await response.json() }
  else {
    return { error: 'Error', msg: "Qualcosa è andato storto. Riprovare" }
  }
}

const API = { login, logout, getHikes, createHike, signin, getAllHikes };
export default API;
