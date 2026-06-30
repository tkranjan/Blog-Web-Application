import { useState } from "react"
import api from "../../api/axios"


function Register() {

  const [formData, setFormData] = useState({

    username: "",

    email: "",

    first_name: "",

    last_name: "",

    password: "",
  })


  const handleChange = (e) => {

    setFormData({

      ...formData,

      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {

  e.preventDefault()

  try {

    const response = await api.post(

      "register/",

      formData
    )

    console.log(response.data)

    alert("Registration Successful")

  }

  catch (error) {

    console.log(error.response.data)

    alert("Registration Failed")
  }
 }


  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-purple-100 p-8 rounded-xl shadow-lg w-full max-w-md">

        <h1 className="text-4xl font-bold text-center mb-6">

          Register

        </h1>


        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-4"
        >

          <input
            type="text"
            name="username"
            placeholder="Username"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="email"
            name="email"
            placeholder="Email"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <button
            type="submit"
            className="bg-black text-white p-3 rounded-lg hover:bg-gray-800"
          >

            Register

          </button>

        </form>

      </div>

    </div>
  )
}

export default Register