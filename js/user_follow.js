const follow = document.querySelector('#follow');
const form = document.getElementById("form")
const submitButton = document.getElementById("submit-button")

submitButton.onclick = () => {
  const formData = new FormData(form)
  const action = form.getAttribute("action")
  const options = {
    method: 'POST',
    body: formData,
  }
  
  fetch(action, options).then((e) => {
    if(e.status === 200) {

      if (follow.textContent == 'Unfollow')
      {
        console.log(form);
        follow.textContent = 'Follow';
        alert("0")                 
      }
      else
      {
        console.log(form);
        follow.textContent = 'Unfollow';
        alert("1")
      }

      alert("保存しました。")
      return
    }
    alert("保存できませんでした。")
  })
}