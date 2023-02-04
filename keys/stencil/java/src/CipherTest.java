package src;

import java.util.Arrays;
import java.util.Random;

public class CipherTest {
	private static void testSanity() {
		Random r = new Random(254922686);
		byte[] m = new byte[8];
		for (int i = 0; i < 100; i++) {
			int k = r.nextInt();
			for (int j = 0; j < 100; j++) {
				r.nextBytes(m);
				byte[] c = Cipher.encrypt(k, new ByteArrayWrapper(m)).getByteArray();
				byte[] mm = Cipher.decrypt(k, new ByteArrayWrapper(c)).getByteArray();
				if (!Arrays.equals(m, mm)) {
					System.out.printf("D(k, E(k, m)) != m for k:%d, m:%s, c:%s, m':%s\n",
						k, bytesToHex(m), bytesToHex(c), bytesToHex(mm));
				}
			}
		}
	}

	private static void testSanityDouble() {
		Random r = new Random(343021410);
		byte[] m = new byte[8];
		for (int i = 0; i < 100; i++) {
			int k1 = r.nextInt();
			int k2 = r.nextInt();
			for (int j = 0; j < 100; j++) {
				r.nextBytes(m);
				byte[] c = Cipher.doubleEncrypt(k1, k2, new ByteArrayWrapper(m)).getByteArray();
				byte[] mm = Cipher.doubleDecrypt(k1, k2, new ByteArrayWrapper(c)).getByteArray();
				if (!Arrays.equals(m, mm)) {
					System.out.printf("D(k, E(k, m)) != m for k:(%d, %d), m:%s, c:%s, m':%s\n",
						k1, k2, bytesToHex(m), bytesToHex(c), bytesToHex(mm));
				}
			}
		}
	}

	public static void main(String[] args) {
		System.out.println("testSanity...");
		testSanity();
		System.out.println("testSanityDouble...");
		testSanityDouble();
	}

	// http://stackoverflow.com/a/9855338/836390
	final protected static char[] hexArray = "0123456789ABCDEF".toCharArray();
		public static String bytesToHex(byte[] bytes) {
    	char[] hexChars = new char[bytes.length * 2];
    	for ( int j = 0; j < bytes.length; j++ ) {
        	int v = bytes[j] & 0xFF;
        	hexChars[j * 2] = hexArray[v >>> 4];
        	hexChars[j * 2 + 1] = hexArray[v & 0x0F];
    	}
    	return new String(hexChars);
	}
}
