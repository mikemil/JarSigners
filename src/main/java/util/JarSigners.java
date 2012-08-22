package util;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipException;
import java.util.zip.ZipFile;

/**
 *  Show which jars are signed with which code signing certificates
 */
public class JarSigners {

	private String folderName;
	private Map<String, List<String>> map;
	private Set<String> certs;
	
	public JarSigners(String folderName) {
		this.folderName = folderName;
		map = new HashMap<String, List<String>>();
		certs = new HashSet<String>();
	}
	
	public void listJarSigners() throws ZipException, IOException {
		File dir = new File(folderName);
		FilenameFilter filter = new FilenameFilter() {
		    public boolean accept(File dir, String name) {
		        return name.endsWith(".jar");
		    }
		};
		String[] files = dir.list(filter);
		System.out.println("Found "+files.length+" files in folder: "+folderName);
		for (String fileName : files) {
			checkJarForCertificate(fileName);
		}
		System.out.println("Certificates used to sign the jars: "+certs);
		if (certs.size() > 1) {
			System.out.println("WARNING: More that one certificate shows up in the jars!");
		}
		System.out.println("Details jar->certificate: "+map);
	}
	
	private void checkJarForCertificate(String fileName) throws ZipException, IOException {
		File jar = new File(folderName, fileName);
		ZipFile zip = new ZipFile(jar);
		//System.out.println("Processing "+fileName);
		for (Enumeration entries = zip.entries(); entries.hasMoreElements();) {
	        // Get the entry name
	        String zipEntryName = ((ZipEntry)entries.nextElement()).getName();
	        if (zipEntryName.endsWith(".RSA")) {
	        	if (!certs.contains(zipEntryName)) {
	        		certs.add(zipEntryName);
	        	}
	        	if (map.containsKey(fileName)) {
	        		List<String> list = map.get(zipEntryName);
	        		list.add(zipEntryName);
	        	} else {
	        		List<String> list = new ArrayList<String>();
	        		list.add(zipEntryName);
	        		map.put(fileName, list);
	        	}
	        }
	    }
		zip.close();
		
	}

	/**
	 * @param args
	 * @throws IOException 
	 * @throws ZipException 
	 */
	public static void main(String[] args) throws ZipException, IOException {
		if (args.length != 1) {
			System.out.println("Invalid invocation: you must pass a folder name");
			return;
		}
		JarSigners js = new JarSigners(args[0]);
		js.listJarSigners();
		System.out.println("Done!");
	}

}
