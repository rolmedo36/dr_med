const listarClientes=async(inCliente) =>{
    try{
        const response=await fetch(`/get_clientes/${inCliente}`);
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            opciones += "<option value=''>Seleccione cliente..</option>";
            data.clientes.forEach((cliente) => {
                opciones += `<option value='${cliente.id}'>${cliente.nombre} - ${cliente.correo}</option>`;
            });
            cboClientes.innerHTML=opciones;
        }else{
            console.log('..')
//            alert("Clientes no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
};
const listarMedicos=async() =>{
    try{
        const response=await fetch("/get_medicos");
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            opciones += "<option value=''>Seleccione médico..</option>";
            data.medicos.forEach((medico) => {
                opciones += `<option value='${medico.id}'>${medico.nombre}</option>`;
            });
            cboMedicos.innerHTML=opciones;
            alert("Seleccione Médico !!")
        }else{
            alert("Médicos no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
};

const cargaInicial=async()=>{
    await listarMedicos();
    await listarClientes();

    inCliente.addEventListener("change", (event) => {
        listarClientes(inCliente.value);
    });
};

window.addEventListener("load", async () => {
    await cargaInicial();
});
