<template>
    <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow class="justify-content-center">
          <CCol :md="5">
            <CCardGroup>
              <CCard class="p-4">
                <CCardBody>
                  <CForm>
                    <h1>Восстановление пароля</h1>
                    <p class="text-medium-emphasis">
                        Введите адрес электронной почты, вам будет выслана ссылка для восстановления пароля.
                    </p>
                    <CInputGroup class="mb-3">
                      <CInputGroupText>
                        <CIcon icon="cil-user" />
                      </CInputGroupText>
                      <CFormInput
                        placeholder="Электронная почта"
                        autocomplete="email"
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol :xs="6">
                        <CButton color="primary" class="px-4"> ОК </CButton>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ForgotPassword',
  }
  </script>