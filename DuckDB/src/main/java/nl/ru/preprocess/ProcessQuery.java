package nl.ru.preprocess;

import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class ProcessQuery {

    private static void writeTitlesToFile(String inputfile, String outputfile) throws IOException {
        FileReader fileReader = new FileReader(inputfile);
        FileWriter fileWriter = new FileWriter(outputfile);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        String line = bufferedReader.readLine();
        while (line != null && line != "" && line != " ") {
            String preprocessed_query = titleToString(line);
            fileWriter.write(preprocessed_query + "\n");
            line = bufferedReader.readLine();
        }
        fileReader.close();
        fileWriter.close();
    }

    private static String titleToString(String query) throws IOException {
        List<String> result = new ArrayList<>();
        Analyzer analyzer = new EnglishStemmingAnalyzer("porter", EnglishAnalyzer.ENGLISH_STOP_WORDS_SET);

        TokenStream tokenStream = analyzer.tokenStream(null, new StringReader(query));
        CharTermAttribute cattr = tokenStream.addAttribute(CharTermAttribute.class);

        tokenStream.reset();
        while(tokenStream.incrementToken()) {
            if (cattr.toString().length() == 0) {
                continue;
            }
            result.add(cattr.toString());
        }
        tokenStream.end();
        tokenStream.close();

        StringBuilder pro = new StringBuilder();
        for (String r: result) {
            pro.append(r);
            pro.append(" ");
        }
        return pro.toString();
    }

    private String titleToString(String[] args) throws IOException {
        StringBuilder query = new StringBuilder();
        for (String arg: args) {
            query.append(arg);
            query.append(" ");
        }

        List<String> result = new ArrayList<>();
        Analyzer analyzer = new EnglishStemmingAnalyzer("porter", EnglishAnalyzer.ENGLISH_STOP_WORDS_SET);

        TokenStream tokenStream = analyzer.tokenStream(null, new StringReader(query.toString()));
        CharTermAttribute cattr = tokenStream.addAttribute(CharTermAttribute.class);

        tokenStream.reset();
        while(tokenStream.incrementToken()) {
            if (cattr.toString().length() == 0) {
                continue;
            }
            result.add(cattr.toString());
        }
        tokenStream.end();
        tokenStream.close();

        StringBuilder pro = new StringBuilder();
        for (String r: result) {
            pro.append(r);
            pro.append(" ");
        }
        return pro.toString();
    }

    public static void main(String[] args) throws IOException {
        String titlesfile = "D:\\Daan\\IR\\olddog\\src\\main\\python\\titles.txt";
        String outputfile = "D:\\Daan\\IR\\olddog\\src\\main\\python\\preprocessed_titles.txt";
        writeTitlesToFile(titlesfile, outputfile);
    }
}
