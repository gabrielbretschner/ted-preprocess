import argparse
import xml.dom.minidom


def main():
    opts = argparse.ArgumentParser()
    opts.add_argument("--src-xml", "-s", help="path to source xml", required=True)
    opts.add_argument("--tgt-xml", "-t", help="path to target xml", required=True)
    opts.add_argument("--src-out", help="path to source output", required=True)
    opts.add_argument("--tgt-out", help="path to target output", required=True)

    args = opts.parse_args()

    src_xml = xml.dom.minidom.parse(args.src_xml)
    tgt_xml = xml.dom.minidom.parse(args.tgt_xml)
    src_docs = {src_doc.getAttribute("docid"): src_doc for src_doc in src_xml.getElementsByTagName("doc")}
    tgt_docs = {tgt_doc.getAttribute("docid"): tgt_doc for tgt_doc in tgt_xml.getElementsByTagName("doc")}
    num_sentences = 0
    num_docs = 0
    with open(args.tgt_out, "w") as tgt_fp, open(args.src_out, "w") as src_fp:
        matching_docs = set(src_docs.keys()) & set(tgt_docs.keys())
        for doc_id in sorted(matching_docs):
            src_seqs = {seq.getAttribute("id"): seq for seq in src_docs[doc_id].getElementsByTagName("seg")}
            tgt_seqs = {seq.getAttribute("id"): seq for seq in tgt_docs[doc_id].getElementsByTagName("seg")}
            for idx in sorted(set(src_seqs.keys()) & set(tgt_seqs.keys())):
                src_string = src_seqs[idx].firstChild.nodeValue
                tgt_string = tgt_seqs[idx].firstChild.nodeValue
                src_fp.write("{}\n".format(src_string.strip()))
                tgt_fp.write("{}\n".format(tgt_string.strip()))
                num_sentences += 1
            num_docs += 1
    print("Processed {} parallel docs out of {} {} src, tgt docs respectively".format(
        num_docs,
        len(src_docs),
        len(tgt_docs))
    )
    print("Written {} sentences to {} and {}".format(num_sentences, args.src_out, args.tgt_out))


if __name__ == '__main__':
    main()
