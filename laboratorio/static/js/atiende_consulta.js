const turno_num = document.getElementById('turno_num');

const buscaTurno=async(turno_num) =>{
    try{
        const response=await fetch(`/get_buscaturno/${turno_num}`);
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            // opciones += "<option value=''>Seleccione cliente..</option>";
            data.clientes.forEach((cliente) => {
                // opciones += `<option value='${cliente.id}'>${cliente.nombre} - ${cliente.correo}</option>`;
                vcliente = cliente;
            });
            cliente_nombre.value=vcliente;
            cliente_nombre2.value=vcliente;
        }else{
            alert('Turno incorrecto !!!');
            document.getElementById('turno_num').focus();
            console.log('..')
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
            //alert("Seleccione Médico !!")
        }else{
            alert("Médicos no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
};

const cargaInicial = async () => {
    await listarMedicos();

    turno_num.addEventListener("change", (event) => {
        buscaTurno(turno_num.value); // Trigger on change of turno_num
    });
};

window.addEventListener("load", async () => {
    await cargaInicial();
});


