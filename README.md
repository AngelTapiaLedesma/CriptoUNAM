# PatchProof 🔐

**A verifiable bug bounty platform powered by Stellar**

PatchProof es una plataforma para gestionar programas de **bug bounty** de forma más transparente entre empresas e investigadores de seguridad.

La idea parte de un problema de confianza: un investigador necesita tener evidencia de que su reporte fue recibido y que la recompensa prometida existe, mientras que una empresa necesita gestionar estos reportes sin exponer información sensible sobre sus sistemas.

PatchProof utiliza **Stellar** como una capa de verificación para registrar eventos importantes del proceso, como el envío de un reporte, su validación y el pago de una recompensa.

La vulnerabilidad completa nunca se publica en blockchain. En su lugar, se genera una huella criptográfica del reporte que permite comprobar su existencia sin revelar su contenido.

---

## 💡 ¿Cómo funciona?

```text
Empresa crea un bounty
        ↓
Investigador envía un reporte
        ↓
PatchProof genera evidencia verificable
        ↓
El reporte es validado
        ↓
Se libera la recompensa
        ↓
La vulnerabilidad puede marcarse como corregida