
const listarDisponible=async(idConsultorio, fecha) =>{
    try{
        const response=await fetch(`/get_disponible/${idConsultorio}/${fecha}`);
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            data.disponibles.forEach((disponible) => {
                opciones += '"' + disponible + '",';
            });
            txtOpciones.innerText='[' + opciones + '""]';
        }else{
            alert("Disponible no encontrados...");
        }
    } catch (error){
        console.log(error);
    }
};

const listarConsultorios=async() =>{
    try{
        const response=await fetch("/get_consultorios");
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            opciones += "<option value=''>Seleccione consultorio..</option>";
            data.consultorios.forEach((consultorio) => {
                opciones += `<option value='${consultorio.id}'>${consultorio.nombre}</option>`;
            });
            cboConsultorio.innerHTML=opciones;
        }else{
            alert("Consultorios no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
    try{
        const response=await fetch("/get_servicios");
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            opciones += "<option value=''>Seleccione servicio..</option>";
            data.servicios.forEach((servicio) => {
                opciones += `<option value='${servicio.id}'>${servicio.nombre}</option>`;
            });
            cboServicios.innerHTML=opciones;
        }else{
            alert("Servicios no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
};

const cargaInicial=async()=>{

    await listarConsultorios();

    cboConsultorio.addEventListener("change", (event) => {
        listarDisponible(cboConsultorio.value, txtFecha.value);
    });
/*    txtFecha.addEventListener("change", (event) => {
        if (cboConsultorio.value == ""){
            alert("Seleccionar consultorio...")
        }else{
            listarDisponible(cboConsultorio.value, txtFecha.value);
        }
    });*/
};

window.addEventListener("load", async () => {
    await cargaInicial();
});
