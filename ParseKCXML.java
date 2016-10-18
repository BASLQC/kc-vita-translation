/*
 * ParseKCXML
 * 
 * MIT License
 *
 * Copyright (c) 2016 limyz
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
*/

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.io.StringReader;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.CharacterData;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

public class ParseKCXML {
  public static void main(String arg[]) throws Exception{
    FileInputStream in = new FileInputStream(new File("mst_mission2.xml"));
    Reader reader = new InputStreamReader(in, "UTF-8");
    InputSource is = new InputSource(reader);
        is.setEncoding("UTF-8");
    
    DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
    Document doc = db.parse(in);
    NodeList nodes = doc.getElementsByTagName("mst_mission2");
    
    BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("mst_mission2.txt"), "UTF-8"));
    
    for (int i = 0; i < nodes.getLength(); i++) {
      Element element = (Element) nodes.item(i);

      NodeList id = element.getElementsByTagName("Id");
      Element line = (Element) id.item(0);
      
      System.out.println("Id: " + getCharacterDataFromElement(line));
      bw.write(line.getTextContent());
      bw.newLine();
      
      NodeList name = element.getElementsByTagName("Name");
      line = (Element) name.item(0);
      
      System.out.println("Name: " + getCharacterDataFromElement(line));
      bw.write(line.getTextContent());
      bw.newLine();

      NodeList details = element.getElementsByTagName("Details");
      line = (Element) details.item(0);
      
      System.out.println("Details: " + getCharacterDataFromElement(line));
      bw.write(line.getTextContent());
      bw.newLine();
      bw.newLine();
    }
    
    bw.flush();
    bw.close();
  }

  public static String getCharacterDataFromElement(Element e) {
    Node child = e.getFirstChild();
    if (child instanceof CharacterData) {
      CharacterData cd = (CharacterData) child;
      return cd.getData();
    }
    return "";
  }
}